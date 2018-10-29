import click

@click.group()
def word_cli():
    pass

@word_cli.command()
def cmd1():
    '''Command on word_cli'''
    click.echo('word_cli cmd1')

@word_cli.command()
def cmd2():
    '''Command on word_cli'''
    click.echo('word_cli cmd2')

if __name__ == '__main__':
    word_cli()
