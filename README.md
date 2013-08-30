# Abuse

Abuse is a mocking program for Python.
Abuse helps you to randomly generate abusive sentences based on the grammar you give it.

If you were looking for a mocking framework for Python to help you write tests,
you might be interested in [Funk](https://github.com/mwilliamson/funk) instead.

## Usage

Abuse accepts context-free grammars, such as:

```
$SENTENCE -> I hate you!
$SENTENCE -> You smell of $SMELL
$SMELL -> elderberries
$SMELL -> dogfood
$SENTENCE -> You're as $RUDE_ADJ as my $PET
$RUDE_ADJ -> stupid
$RUDE_ADJ -> ugly
$PET -> dog
$PET -> rat
```

Given the path to a file containing a context-free grammar in this format,
Abuse can generate a random phrase:

```
$ python/generate-abuse.py EXAMPLE 
You smell of elderberries
```

Abuse can also generate all possible sentences:

```
$ ./generate-abuse.py EXAMPLE --all
I hate you!
You smell of elderberries
You smell of dogfood
You're as stupid as my dog
You're as stupid as my rat
You're as ugly as my dog
You're as ugly as my rat</pre>
```
