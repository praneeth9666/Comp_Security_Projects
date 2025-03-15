#
#  Note: You must run ./setcookie before running make.
#

CC := gcc
CFLAGS := -w -m32 -static -U_FORTIFY_SOURCE -fno-pie -DCOOKIE=$(shell cat cookie) -g
LDFLAGS :=
LDLIBS :=

targets := target0 target1 target2 target3 target4 target5 target6 target7 target8 target9

.PHONY: default clean install uninstall

default: $(targets) permissions

target0: CFLAGS += -fno-stack-protector -z execstack 
target1: CFLAGS += -fno-stack-protector -z execstack 
target2: CFLAGS += -fno-stack-protector -z execstack 
target3: CFLAGS += -fno-stack-protector -z execstack 
target4: CFLAGS += -fno-stack-protector -z execstack
target5: CFLAGS += -fno-stack-protector
target6: CFLAGS += -fno-stack-protector -z execstack
target7: CFLAGS += -fno-stack-protector -z execstack
target8: CFLAGS += -fno-stack-protector
target9: CFLAGS += -fno-stack-protector -z execstack

target0: target0.c helper.c
target1: target1.c helper.c
target2: target2.c helper.c
target3: target3.c helper.c
target4: target4.c helper.c
target5: target5.c helper.c
target6: target6.c helper.c
target7: target7.c helper.c
target8: target8.c helper.c
target9: target9.c helper.c

clean:
	rm -f $(targets)

permissions:
	sudo setcap cap_setuid+ep target2
	sudo setcap cap_setuid+ep target3
	sudo setcap cap_setuid+ep target4
	sudo setcap cap_setuid+ep target5
	sudo setcap cap_setuid+ep target6
	sudo setcap cap_setuid+ep target7
	sudo setcap cap_setuid+ep target8
	sudo setcap cap_setuid+ep target9
	#sudo chown root:ubuntu target[23456789]
	#sudo chmod 6777 target[23456789]
