# CLI
Command-line interpreter for bash commands.
Supported commands:
```
echo - display a line of text
cat - concatenate files and print on the standard output
wc - print newline, word, and byte counts for each file
pwd - print name of current/working directory
exit - cause normal process termination
external - all another command, but via running bush 

Also combinations of this commands - pipelines (ex. echo line | wc), variable substitution (ex. cat $filename)
and variable assignment (ex. x=3)
```
## Usage
1) From root directory run cli:
```bash
python3 main.py
```
2) Write command to command line:
```bash
cat $filename | wc
```
3) Receive the result:
```bash
38  124  1267
```
3) Run another command or exit to stop cli:
```bash
exit
```

## Architecture
![Data flow diagram](https://raw.githubusercontent.com/wiki/tiginamaria/SoftwareDesign/images/CLI.png)

1) **CLI** reads the input from command line and delegate it's interpretation to **Pipeline** object. 
2) Class Pipeline use pipeline pattern to run **Substituter**, **Parser** and **Interpreter** in sequence so as to give the output of previous phase as input for the next phase.
3) **Substituter** splits the input sting to tokens **VariableSubstitution**, **NoQuotes**, **SingleQuotes**, **DoubleQuotes**, process substitution of **VariableSubstitution** and concatenate the result into single string. All varibales stores in **Environment** object.
```python
NoQuotes = '[^$'"]*'
SingleQuotes = '[^']*'
DoubleQuotes = "[[^$"]+|VariableSubstitution]*"
VariableSubstitution = $[_a-zA-Z][_a-zA-Z0-9]*
```
4) **Parser** splits input from **Substituter** to tokens **PipeToken**, **AssignmentToken** and delegate building of **ExecutableCommand** from **AssignmentToken** and **CommandToken** to **CommandFactory**.
```python
NoQuotes = '[^'"]*'
SingleQuotes = '[^']*'
DoubleQuotes = "[^"]*"
ArgumentToken = [NoQuotes|SingleQuotes|DoubleQuotes]+
CommandToken = name() (ArgumentToken)*
PipeToken = CommandToken (|CommandToken)*
AssignmentToken = Variable=ArgumentToken
Variable = [_a-zA-Z][_a-zA-Z0-9]*
```
To parse tokens I used [pyPEG](https://fdik.org/pyPEG/) libary.
5) **Interpreter** execute list of **ExecutableCommand** one by one giving outpur_stream as input_stream for every next command. **ExecutableCommand** object is abstact calss for all commands (**Cat**, **Echo**, ...) which has .execute(). Every command is given outpur_stream, input_stream and return code meaning status o execution.
