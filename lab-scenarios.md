# Lab scenarios

## 1 · The lab itself works
Open a new pane in the lab workspace.
Run ls -la in that pane.
Read the pane's text back.
Close the pane.
Expect: the output of ls -la is on screen, and after closing, the pane is no longer in the pane list.

## 2 · The harness runs in the lab
Open a new pane in the lab workspace.
Start the harness in that pane.
Send it one short prompt: Reply with exactly: lab ok
Expect: the harness starts, and its reply contains the text lab ok.
Close the pane.

## 3 · Extensions carry over
Start the harness in a lab pane and send it one short prompt.
Run split in a second pane, or the command that starts a split.
Does a new pane show up?
Does it end with the split notice?
