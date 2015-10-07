title: Emacs navigation options
date: 2015-08-03 19:14:00
status: published
tags: emacs, linux
lang: en

[TOC]

If you don’t have an emacs editor, install emacs editor as we discussed earlier.

Notation used in this article:

C-a : Ctrl-a
M-a : Meta-a ( If you don’t have Meta key, use Esc key )
C-M-a : Ctrl-Meta-a

### 1.  Emacs Line Navigation ###

Following four navigation can be done line by line.

C-p : go to previous line
C-n : go to next line
C-f : go forward one character
C-b : go backward one character

Repeat factor

By using the repeat factor in EMACS we can do this operation for N times. For example, when you want to go down by 10 lines, then type C-u 10 C-p

Within a line if you want to navigate to different position, you have following two options.

C-a : go to the starting of the current line.
C-e : go to the end of the current line.

At thegeekstuff, we love Vim editor. We’ve written lot of articles on Vim editor. If you are new to the Vim editor, refer to our Vim editor navigation fundamentals article.

### 2. Emacs Screen Navigation ###

Following three navigation can be done in relation to text shown in the screen.

C-v : Jump forward one full screen.
M-v : Jump backwards one full screen. ( If you dont have Meta key, use ESC key )
C-l : Make the current line as center line of window.

You can also use Page Up, Page Down for screen navigation.

### 3. Emacs Special Navigation ###

Following are couple of special navigation that are used to go to the start or end of buffer.

M-< : Go to the start of file
M-> : Go to the end of file

### 4. Emacs Word Navigation ###

Following are two word navigation keys.

M-f : navigate a word forward.
M-b : navigate a word backward.

### 5. Emacs Paragraph Navigation ###

M-a : Go to the beginning of the current paragraph. By pressing M-a again and again move to the previous paragraph beginnings.
M-e : Go to the end of the current paragraph. By pressing M-e again and again move to the next paragraph end, and again.

### 6. Emacs Search Navigation ###

When you want to search by giving the plain text,

C-s : Type Ctrl+s followed by the word to Search. Press Ctrl+s continuously to move to the next occurrences. Press enter to terminate search.
C-r : Do a reverse search. All other explanation are like Ctrl+s

When you want to search using regular expression,

C-M-s : Type Ctrl+s followed by the regex to Search. Press Ctrl+s continuously to move to the next occurrences. Press enter to terminate search.
C-M-r : Do a reverse search. All other explanation are like Ctrl+Meta+s

### 7. Emacs Navigation from Command Line ###

Emacs +N filename: Go to the Nth line of the file after opening it.

$ emacs +10 /etc/passwd
