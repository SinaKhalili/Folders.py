![Folders.py](https://socialify.git.ci/sinakhalili/Folders.py/image?description=1&descriptionEditable=Implementation%20of%20the%20Folders%20%F0%9F%93%82%20esoteric%20programming%20language%2C%20a%20language%20with%20no%20code%20and%20just%20folders.&font=Inter&language=1&logo=https%3A%2F%2Fsocialify.git.ci%2Fsinakhalili%2FFolders.py%2Fimage%3Fdescription%3D1%26descriptionEditable%3DImplementation%2520of%2520the%2520Folders%2520%25F0%259F%2593%2582%2520esoteric%2520programming%2520language%252C%2520a%2520language%2520with%2520no%2520code%2520and%2520just%2520folders.%26font%3DInter%26language%3D1%26logo%3Dhttps%253A%252F%252Fsocialify.git.ci%252Fsinakhalili%252FFolders.py%252Fimage%253Fdescription%253D1%2526descriptionEditable%253DImplementation%252520of%252520the%252520Folders%252520%2525F0%25259F%252593%252582%252520esoteric%252520programming%252520language%25252C%252520a%252520language%252520with%252520no%252520code%252520and%252520just%252520folders.%2526font%253DInter%2526language%253D1%2526logo%253Dhttps%25253A%25252F%25252Fsocialify.git.ci%25252Fsinakhalili%25252FFolders.py%25252Fimage%25253Fdescription%25253D1%252526descriptionEditable%25253DImplementation%25252520of%25252520the%25252520Folders%25252520%252525F0%2525259F%25252593%25252582%25252520esoteric%25252520programming%25252520language%2525252C%25252520a%25252520language%25252520with%25252520no%25252520code%25252520and%25252520just%25252520folders.%252526font%25253DInter%252526language%25253D1%252526pattern%25253DPlus%252526theme%25253DLight%2526pattern%253DPlus%2526theme%253DLight%26pattern%3DPlus%26theme%3DLight&pattern=Plus&theme=Light)

# Folders.py

<img src="https://gist.githubusercontent.com/SinaKhalili/5384cae0c5a448c95099ca4bb573a774/raw/a0f7df8724eebec50b630b836445418617f66c0f/folders_gif.gif" align="right"
     alt="A deep folders zoom" width="250">

Folders is an esoteric programming language, [created by Daniel Temkin](http://danieltemkin.com/Esolangs/Folders/) in 2015, which encodes the program _entirely_ into the **directory structure**.

All names of the folders as well as their contents are completely ignored. Instead, the commands
are encoded in the nesting of folders within folders.

Let me say that again: THE SOURCE CODE IS THE DIRECTORY STRUCTURE. Lol. 

This is a Python implementation of Folders for all to enjoy!

Folders is (was originally) implemented in [C#](https://github.com/rottytooth/Folders).

## Usage

### Install from pip
Simply install the `Folders` command line interpreter
```
pip install Folders
```

Give the folder of the program you wish to run as an command line argument

```
Folders sample_programs/HelloWorld
# => Hello, World!
```

If instead you would like list the Python code to stdout, use the `-l` option

```
Folders -l sample_programs/Fibonacci
# => print("Hello, World!", end='', flush=True)
```

### Run python
The implementation is just the python file, [folders.py](./folders/folders.py) and has no dependencies, so if you'd like you can clone the repo and run `python ./folders/folders.py` instead of pip installing and use it the same as in the examples above.



## Language details

The language details are on the [esolangs wiki](https://esolangs.org/wiki/Folders), but I've put it here for reference.

For example, take a look at the [Fibonacci sample program](./sample_programs/Fibonacci).

The root folder contains a list of _command folders_ - in this case labelled `Nf1..`, `Nf2..`, but the names don't actually matter except the alphabetical ordering - the first folder (which I've labelled with an `init`) is the first "sub-folder", the next is the second, etc.

### Commands:

Commands take the following form
| Command | # of folders | Details |
| ------- | ------------ | ----------------------------------------------------------------------------------------------------------- |
| if | 0 folders | Second sub-folder holds expression, third holds list of commands |
| while | 1 folder | Second sub-folder holds expression, third holds list of commands |
| declare | 2 folders | Second sub-folder holds type, third holds var name (in number of folders, ex. zero folders becomes "var_0") |
| let | 3 folders | Second sub-folder hold variable name (in number of folders), third holds an expression |
| print | 4 folders | Second sub-folder holds expression |
| input | 5 folders | Second sub-folder holds variable name | 

### Expressions:

Expression folders take the following form:
| Type | # of folders | Details |
|---------------|-----------|-----------------------------------------------------------------------------------------------------------|
| Variable | 0 folders | Second sub-folder holds variable name |
| Add | 1 folder | Second sub-folder holds the first expression to add, third holds second expression |
| Subtract | 2 folders | Second sub-folder holds the first expression to subtract, third holds second expression |
| Multiply | 3 folders | Second sub-folder holds the first expression to multiply, third holds second expression |
| Divide | 4 folders | Second sub-folder holds the first expression to divide, third holds second expression |
| Literal Value | 5 folders | Second sub-folder holds the type of the value (as described by types below, ex. two folders for a string) |
| Equal To | 6 folders | Second and third folders hold expressions to compare |
| Greater Than | 7 folders | Second and third folders hold expressions to compare (takes the form : second folder > third folder) |

### Types

And finally type folders take the following form:

| Type   | # of folders |
| ------ | ------------ |
| int    | 0 folders    |
| float  | 1 folder     |
| string | 2 folders    |
| char   | 3 folders    |

### Note on this implemementation

The `int`, `float`, and `char` types are 8-bit only. But, you can add into their variables to arbitrary length, so to get a very large number you can simply multiply it a bunch of times.

This is what the fibonacci program does.

## The absolute power of folders

Behold, the mighty Truth Machine program:

![truth_machie](truth_machine.png)

## A mighty meme-worthy point

_All Folders programs are 0 bytes_ if you're on windows as it interprets an empty folder as 0 bytes.

The ultimate code golf!

## Links

- [Folders on esolang](https://esolangs.org/wiki/Folders)
- [Folders homepage](http://danieltemkin.com/Esolangs/Folders/)
