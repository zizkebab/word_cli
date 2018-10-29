import click

@click.group()
def word_cli():
    pass

# @word_cli.command()
# @click.argument('f', type=click.Path(exists=True))
# def divide():
#     '''divide a file into to files: one with odds and one with evens'''
#     click.echo('divide a file into to files: one with odds and one with evens')

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
