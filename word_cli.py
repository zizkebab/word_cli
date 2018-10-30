import click
import itertools
import re
import in_place
import logging
import click_log


# Adding a logger and using click_log
logger = logging.getLogger(__name__)
click_log.basic_config(logger)

@click.group()
def word_cli():
    pass


@word_cli.command()
@click.argument('f', type=click.Path(exists=True), required=1)
@click_log.simple_verbosity_option(logger)
def divide(f):
    '''divide a file into to files: one with odds and one with evens'''
    logger.debug("Dividing {0} into {0}_odd and {0}_even".format(f))
    try:
        output_odd = open(f + "_odd", "w")
        logger.debug("opened {0}".format(output_odd))
        output_even = open(f + "_even", "w")
        logger.debug("opened {0}".format(output_even))
        with open(f, "r") as input:
            for word in input.read().split():
                if len(word) % 2 == 0:
                    logger.debug("{0} is even lengthed".format(word))
                    output_even.write(word + ", ")
                else:
                    logger.debug("{0} is odd lengthed".format(word))
                    output_odd.write(word + ", ")

        output_odd.close()
        logger.debug("closed {0}".format(output_odd))
        output_even.close()
        logger.debug("closed {0}".format(output_even))
    except IOError as e:
        logger.exception("Oh my god IOError!!!111")



@word_cli.command()
@click.argument('input', type=click.STRING, required=1)
@click_log.simple_verbosity_option(logger)
def reverse(input):
    '''reverse a given string'''

    ''' builtin extended slicing to reverse'''
    logger.debug("input string is {0}".format(input))
    reversed = input[::-1]
    click.echo(reversed)

@word_cli.command()
@click.argument('file1', type=click.Path(exists=True), required=1)
@click.argument('file2', type=click.Path(exists=True), required=1)
@click_log.simple_verbosity_option(logger)
def merge(file1, file2):
    '''merge two files according to heuristics by Lioz. I assume that separating text file contents by white space
    is legit.'''
    output_path = "{0}_{1}".format(file1, file2)
    click.echo('merge {0} and {1} into {2} according to heuristics by Lioz'.format(file1, file2, output_path))
    with open(output_path, "w") as output_merge:

        # afaik zip_longest is something nice and new in python 3. In python2, I should've made something like
        # this: https://flylib.com/books/en/2.9.1.361/1/
        for word, pair in itertools.zip_longest(__get_word_from_file(file1), __get_pair_from_file(file2)):
            logger.debug("unzipped word: {0} and pair: {1}".format(word, pair))
            merged = "{0} {1} ".format(word if word is not None else '',
                                    pair if pair is not None else '')
            logger.debug("merged line: {0}".format(merged))
            output_merge.writelines(merged)


def __get_word_from_file(file_path):
    '''
    opens a file, splits to string by white space, and generates a string iterator
    :param file_path: text file source path
    :return:
    '''
    with open(file_path, "r") as input:
        for word in input.read().split():
            logger.debug("yielded {0}".format(word))
            yield word


def __get_pair_from_file(file_path):
    '''
    opens a file, splits to string by white space, and generates a string iterator of word pairs
    :param file_path: text file source path
    :return:
    '''
    so_called_pair = ""
    counter = 0
    with open(file_path, "r") as input:
        for word in input.read().split():
            counter += 1
            if counter == 2:
                so_called_pair = " ".join((so_called_pair, word))
                counter = 0
                logger.debug("yielding pair: {0}.".format(so_called_pair))
                yield so_called_pair
            else:
                so_called_pair = word

    if counter == 1:
        logger.debug("yielding one last word without a pair: {0}.".format(so_called_pair))
        yield so_called_pair

@word_cli.command()
@click.argument("io_file", type=click.Path(exists=True), required=1)
@click.argument("dict_file", type=click.Path(exists=True), required=1)
@click_log.simple_verbosity_option(logger)
def sub_by_dict(io_file, dict_file):
    '''
    replace input file contents by using a dictionary file
    :param input_file:
    :param dict_file:
    :return:
    '''
    dict = __parse_dict_file(dict_file)
    # sorting dictionary keys by length, using the longest key for replacement
    sorted_keys = sorted(dict.keys(), key=len, reverse=True)
    with in_place.InPlace(io_file) as io:
        for line in io:
            logger.debug("original line: {0}".format(line))
            for key in sorted_keys:
                # there's probably a more efficient method to replace... but this is easy.
                line = re.sub(key, dict[key], line)
            logger.debug("alrtered line: {0}".format(line))
            io.writelines(line)
            logger.debug("written line")

def __parse_dict_file(dict_file):
    dict = {}
    with open(dict_file, "r") as input:
        logger.debug("opened dict file {0}".format(0))
        for line in input.readlines():
            k, v = line.split()
            logger.debug("found k,v {0}, {1}".format(k, v))
            if k in dict:
                logger.debug("key {0} would overwrite existing value {1} with {2}".format(k, dict[k], v))
            dict[k] = v
    logger.info("parsed dict file {0} with {1} pairs".format(dict_file, len(dict.keys())))
    return dict

if __name__ == '__main__':
    word_cli()
