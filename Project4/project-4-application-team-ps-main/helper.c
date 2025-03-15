#include <stdio.h>
#include <stdlib.h>
#include <sys/personality.h>
#include <unistd.h>

#define STACK_GOAL 0xFFFF0000U
#define MAX_PAD 0xFFFF

int main(int argc, char *argv[], char *envp[])
{
	volatile int canary = 0xDEADBEEF;

	setuid(0);

	// Check if ASLR is on. If it is, disable and re-run
	if ((void*)(&canary) < (void*)(0xffffc000)) {
		if (personality(PER_LINUX|ADDR_NO_RANDOMIZE) == -1) {
			perror("Error disabling ASLR");
			return 1;
		}

		//printf("Rerruning...%p\n", &canary);
		//fflush(stdout);
		execve(argv[0], argv, envp);
		perror("Error: execve");
		return 1;
	}

	// Advance the stack pointer to a position that's invariant of
	// the size of the environment and the program arguments.
	char *esp = alloca(0);
	if ((esp < (char *)STACK_GOAL) || (esp - (char *)STACK_GOAL > MAX_PAD)) {
		fprintf(stderr, "Can't normalize stack position: %p\n", esp);
		return 1;
	}
	alloca(esp - (char *)STACK_GOAL);
#ifdef COOKIE
	alloca(COOKIE);
#endif

	int ret = _main(argc, argv, envp);

	if (canary != 0xDEADBEEF) {
		fprintf(stderr, "Uh oh, the canary is dead.\n" \
				"Don't overwrite the stack frame for main().\n");
	}
	return ret;
}
