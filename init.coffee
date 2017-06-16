
atom.commands.add 'atom-text-editor', 'markdown:paste-as-link', ->
  return unless editor = atom.workspace.getActiveTextEditor()

  selection = editor.getLastSelection()
  clipboardText = atom.clipboard.read()

  selection.insertText("[#{selection.getText()}](#{clipboardText})")

atom.commands.add 'atom-text-editor',
  'user:insert-date': (event) ->
    return unless editor = @getModel()
    editor.insertText(new Date().toLocaleString())
