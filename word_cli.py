import click

@click.group()
def word_cli():
    pass


@word_cli.command()
@click.argument('f', type=click.Path(exists=True))
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

# @word_cli.command()
# def merge():
#     '''merge two files according to heuristics by Lioz'''
#     click.echo('merge two files according to heuristics by Lioz')
#

if __name__ == '__main__':
    word_cli()
