# connect-four-with-ai

#### The AI
This is is pretty dumb because it only checks one step forward.

##### The AI checks these rules in order for each column:
1. If the AI wins when it drops a piece in that column, __return__ that column.
2. If the Player wins when he/she drops a piece in that column, append that column to _p_win_cols_.
3. If the AI connects to three when it drops a piece in that column, append that column to _force_cols_.
4. If the Player connects to three when he/she drops a piece in that column, append that column to _p_force_cols_.

##### If nothing was returned, check the following rules in order:
1. If _p_win_cols_ is not empty, choose a random column from it and __return__ that column.
2. If _force_cols_ is not empty, choose a random column from it and __return__ that column.
3. If _p_force_cols_ is not empty, choose a random column from it and __return__ that column.

##### If still nothing is returned:
1. If not all five columns in the middle are full, choose a random non-full column from it and __return__ that column.
2. Randomly choose a non-full column from the other two columns and __return__ that column.

##### What will happen if all of the columns are full?
* It won't happen because in the _Game_ class it will check for draw.

#### Run Game
* No console version: _main_noconsole.pyw_ 
* With console: _main.py_
