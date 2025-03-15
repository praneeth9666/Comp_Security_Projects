from PIL import Image
from facenet_pytorch import InceptionResnetV1   #, MTCNN
from torchvision import datasets, transforms
import numpy as np
import math
import torch
import pickle
import argparse
import json


# LFW functions taken from David Sandberg's FaceNet implementation
def distance(embeddings1, embeddings2, distance_metric=0):
    if distance_metric==0:
        # Euclidian distance
        diff = np.subtract(embeddings1, embeddings2)
        dist = np.sum(np.square(diff),1)
    elif distance_metric==1:
        # Distance based on cosine similarity
        dot = np.sum(np.multiply(embeddings1, embeddings2), axis=1)
        norm = np.linalg.norm(embeddings1, axis=1) * np.linalg.norm(embeddings2, axis=1)
        similarity = dot / norm
        dist = np.arccos(similarity) / math.pi
    else:
        raise 'Undefined distance metric %d' % distance_metric

    return dist

def remove_transparency(im):
    n = np.array(im)
    n = n[:, :, :3]
    return Image.fromarray(n)


# Convert an image to a tensor.
# Resize -> Remove transparency (alpha channel) -> convert to tensor
def im2tensor(img_fn,resize=(160,160)):
    img = Image.open(img_fn)
    return transforms.ToTensor()(remove_transparency(img.resize(resize)))


def main():
    parser = argparse.ArgumentParser(description="Face detection")
    parser.add_argument('--image', type=str, default=None, help='Image to identify')
    parser.add_argument('--raw-embedding', action='store_true', help='If set, outputs the raw embedding')
    parser.add_argument('--compare-embedding', default=None, help='Embedding to compare to, in format: \'[0.000, 0.111, ...]\'')
    parser.add_argument('--compare', type=str, default=None, help='Image to compare against')
    parser.add_argument('--embeddings', type=str, default=None, help='Filename of an embeddings listing to find the closest match against')
    parser.add_argument('--top', type=int, default=5, help='Top N to display when embeddings are provided')
    args = parser.parse_args()

    # Create a face detection pipeline using MTCNN
    # We won't use this for now...
    #mtcnn = MTCNN(image_size=160, margin=14, selection_method='center_weighted_size')

    # Inception resnet
    resnet = InceptionResnetV1(pretrained='vggface2').eval()

    if args.compare is not None:
        # Compare to another image

        # Load images to tensors
        t1 = im2tensor(args.image)
        t2 = im2tensor(args.compare)

        # Compute embeddings
        img_embedding1 = resnet(t1.unsqueeze(0))
        img_embedding2 = resnet(t2.unsqueeze(0))

        #dist = distance(em1, em2)
        dist = torch.cdist(img_embedding1, img_embedding2)
        print(float(dist))

    elif args.embeddings is not None:

        # Load image
        t = im2tensor(args.image)

        # Compute embedding
        embedding = resnet(t.unsqueeze(0))

        faces = {} # name => embedding
        with open(args.embeddings, 'rb') as f:
            faces = pickle.load(f)


        # Check against every face
        # would be faster to do it in one torch.cdist, but this is more intuitive
        dists = []
        for name, emb in faces.items():
            d = float(torch.cdist(emb, embedding))
            dists.append((d, name))

        # Print out results
        i = 1
        for d, name in sorted(dists, key=lambda x: x[0])[:args.top]:
            print('#%d:  %.4f  %s' % (i, d, name))
            i += 1

    elif args.raw_embedding:

        t = im2tensor(args.image)
        emb = resnet(t.unsqueeze(0))
        print(emb[0].tolist())

    elif args.compare_embedding is not None:

        t = im2tensor(args.image)
        emb = resnet(t.unsqueeze(0))

        cmp_emb = torch.tensor(json.loads(args.compare_embedding)).unsqueeze(0)

        dist = torch.cdist(emb, cmp_emb)
        print(float(dist))

    else:
        print('Error: must specify either --compare or --embeddings')
        parser.print_help()


if __name__=='__main__':
    main()
