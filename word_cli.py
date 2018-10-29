import click
import itertools

@click.group()
def word_cli():
    pass


@word_cli.command()
@click.argument('f', type=click.Path(exists=True), required=1)
def divide(f):
    '''divide a file into to files: one with odds and one with evens'''
    click.echo("Dividing {0} into {0}_odd and {0}_even".format(f))
    try:
        output_odd = open(f + "_odd", "w")
        output_even = open(f + "_even", "w")
        with open(f, "r") as input:
            for word in input.read().split():
                if len(word) % 2 == 0:
                    output_even.write(word + ", ")
                else:
                    output_odd.write(word + ", ")

        output_odd.close()
        output_even.close()
    except IOError as e:
        '''TODO: Log/Debug ...'''



@word_cli.command()
@click.argument('input', type=click.STRING, required=1)
def reverse(input):
    '''reverse a given string'''

    ''' builtin extended slicing to reverse'''
    reversed = input[::-1]
    click.echo(reversed)

@word_cli.command()
@click.argument('file1', type=click.Path(exists=True), required=1)
@click.argument('file2', type=click.Path(exists=True), required=1)

def merge(file1, file2):
    '''merge two files according to heuristics by Lioz. I assume that separating text file contents by white space
    is legit.'''
    output_path = "{0}_{1}".format(file1, file2)
    click.echo('merge {0} and {1} into {2} according to heuristics by Lioz'.format(file1, file2, output_path))
    with open(output_path, "w") as output_merge:

        # afaik zip_longest is something nice and new in python 3. In python2, I should've made something like
        # this: https://flylib.com/books/en/2.9.1.361/1/
        for word, pair in itertools.zip_longest(__get_word_from_file(file1), __get_pair_from_file(file2)):
            output_merge.writelines("{0} {1} ".format(word,pair))


def __get_word_from_file(file_path):
    '''
    opens a file, splits to string by white space, and generates a string iterator
    :param file_path: text file source path
    :return:
    '''
    with open(file_path, "r") as input:
        for word in input.read().split():
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
                yield so_called_pair
            else:
                so_called_pair = word

    if counter == 1:
        yield so_called_pair




if __name__ == '__main__':
    word_cli()
