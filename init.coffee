
atom.commands.add 'atom-text-editor', 'markdown:paste-as-link', ->
  return unless editor = atom.workspace.getActiveTextEditor()

  selection = editor.getLastSelection()
  clipboardText = atom.clipboard.read()

  selection.insertText("[#{selection.getText()}](#{clipboardText})")

atom.commands.add 'atom-text-editor',
  'user:insert-date': (event) ->
    return unless editor = @getModel()
    editor.insertText(new Date().toLocaleString())

keyPressed = false;

# neat trick to allow Atom to interpret double-tapping the shift key as a prefix key
# from www.atom-tweaks.com
# Adding this to your init.coffee should allow you to use shift-double in keymaps
# to execute commands by double-tapping either shift key.
# Credit goes to @spaceribs for the code: https://gist.github.com/spaceribs/76b62d6cedb1d0892ec10a8b35d38683

atom.keymaps.addKeystrokeResolver ({event}) ->
  if event.key == "Shift" && event.type == "keydown"
    if keyPressed
      keyPressed = false;
      console.log('keyPressed');
      return 'shift-double';
    else
      keyPressed = true;
      setTimeout (-> keyPressed = false), 200;
      return null;
