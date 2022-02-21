from trie import Trie
from algorithms import match_trie, get_failure_links, get_output_links, get_dna_reverse_complement
import argparse
import time
import os


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('corpus_file', type=str)
    parser.add_argument('pattern_file', type=str)
    parser.add_argument('--output_file', type=str, default='./matches.txt')
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--no_comp', action='store_true')
    parser.add_argument('--comp_file', type=str, default=None)
    args = parser.parse_args()

    corpus_file = args.corpus_file
    pattern_file = args.pattern_file
    verbose = args.verbose
    no_comp = args.no_comp
    output_file = args.output_file
    comp_file = args.comp_file

    if verbose:
        print(f'Reading in corpus file {corpus_file}...')
    with open(corpus_file, 'r') as fr:
        corpus = fr.read()

    if verbose:
        print(f'Reading in pattern file {pattern_file}...')
    with open(pattern_file, 'r') as fr:
        patterns = [pat.lower() for pat in fr.read().split('\n') if pat]

    if verbose:
        print('Searching for following patterns in corpus:')
        print('\n'.join(patterns))

    if verbose:
        print('Constructing trie from patterns...')
    pattern_trie = Trie(patterns)

    if verbose:
        print('Constructing failure links...')
    failure_links = get_failure_links(pattern_trie)

    if verbose:
        print('Constructing output links...')
    output_links = get_output_links(pattern_trie, failure_links)

    if not no_comp:
        if comp_file is not None and os.path.exists(comp_file):
            if verbose:
                print('Reading in corpus complement file...')
            with open(comp_file, 'r') as fr:
                reverse_comp = fr.read()
        else:
            if verbose:
                print('Constructing reverse complement of corpus text...')
            reverse_comp = get_dna_reverse_complement(corpus)

    start = time.time()
    if verbose:
        print('Beginning matching of input corpus...')
    matches = match_trie(corpus, pattern_trie, failure_links, output_links, verbose=verbose)
    matches = [(t + 1, p, 1) for t, p in matches]

    if not no_comp:
        if verbose:
            print('\nBeginning matching of reverse complement...')
        matches_reverse_comp = match_trie(reverse_comp, pattern_trie, failure_links, output_links, verbose=verbose)
        matches_reverse_comp = [(len(reverse_comp) - t - 2, p, 2) for t, p in matches_reverse_comp]
        matches.extend(matches_reverse_comp)
    end = time.time()

    print(f'\nFinished! Matching took {end - start} seconds')

    matches = sorted(matches)

    if verbose:
        print(f'Writing results to output file {output_file}...')
    with open(output_file, 'w') as fw:
        fw.write('\n'.join([f'{m[0]} {m[1]} {m[2]}' for m in matches]))


if __name__ == '__main__':
    main()
