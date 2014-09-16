# README
This plugin lets you modify the numbers in your text document. 

## Use cases
Useful while writing .md files where suppose you are writing a ordered list and you decide to insert a new list element in between. Now you have to increase all the numbers below this element manually. Instead, after installing this plugin, you can do this easily:

1. Select all those lines
2. do a `ctrl-shift-L` to get multiple cursors
3. Press `Home` to go to the start of each line(where I assume the numbers are written)
4. 'ctrl-shift-p' -> "increment numbers"

**P.S**: I know you don't have to write correct numbers in your .md files but I like to keep it clean

Another Use case is when writing snippets. There are `${1}` kind of placeholders. What do you do if you want to insert a placeholder in between? You use my plugin!

## Features

1. **Select Next Number** : `ctrl-shift-P` -> `Select Next Number`. Selects the number immediately next to your cursor position(s)!
2. **Modify Numbers** 
	* **Increment** : `ctrl-shift-P` -> `Increment Numbers`. Increments selected/just next numbers by 1
	* **Decrement** : `ctrl-shift-P` -> `Decrement Numbers`. Decrements selected/just next numbers by 1
	* **Square** : `ctrl-shift-P` -> `Square Numbers`. Squares selected/just next numbers by 1
	* **Double** : `ctrl-shift-P` -> `Double Numbers`. Doubles selected/just next numbers by 1
	* **Sequence**: `ctrl-shift-P` -> `Number Sequence`. Selected numbers are replaced by consecutive numbers, starting with the first value
	* **Accumulation**: `ctrl-shift-P` -> `Accumulate Selected Number(s)`. Selected numbers are replaced by the accumlating sum
	* **Summation**: `ctrl-shift-P` -> `Sum Up Selected Number(s)`. All selected numbers are replace by the total sum
	* **Batch**: `ctrl-shift-P` -> `Batch Number Manipulation`. Selected numbers are computed against the formula. Supported functions are: `sin`, `cos`, `tan`, `log`, `e` and `pi`. The variable `x` will be substituted to the number selected. The variable `i` will be substituted to the index of the selection (started from 0).
	* **Custom Modifications** : bring up the console by ctrl-\` and type 
        
            view.run_command('modify_numbers',{"args":{"modifier_function":(lambda x: x**3)}) #change the function given by the lambda for custom modification
