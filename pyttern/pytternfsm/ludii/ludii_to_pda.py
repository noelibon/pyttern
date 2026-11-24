from ...antlr.ludii.LudiiParser import LudiiParser
from ...antlr.ludii.LudiiParserVisitor import LudiiParserVisitor
from ...simulator.pda.transition import NamedTransition
from ..generic_to_pda import Generic_to_PDA


class Ludii_to_PDA(Generic_to_PDA, LudiiParserVisitor):
    def __init__(self):
        super().__init__(LudiiParser, skippable_nodes=[], remove_double_wildcard=[], tree_pruner=None)
        self._n_wildcards = 0

    def visit(self, tree):
        # the pattern is the single ludeme of the file, without EOF
        if isinstance(tree, LudiiParser.File_inputContext):
            functions = tree.getTypedRuleContexts(LudiiParser.FunctionContext)
            if len(functions) != 1:
                raise ValueError(f"A Luttern pattern must contain exactly one ludeme, found {len(functions)}")
            tree = functions[0]
        return super().visit(tree)

    def define_boundaries(self, ctx):
        n = ctx.getChildCount()
        return n, n

    def visitArgument(self, ctx):
        # '?' is still lexed as a NAME (no wildcard token in the grammar yet)
        if ctx.getText() == "?":
            self._n_wildcards += 1
            label = f"?{self._n_wildcards}"
            self.pda.named_wildcards.add(label)
            return self._add_up_transition(ctx, NamedTransition(label))
        return self.visitChildren(ctx)

    def visitSimple_compound_wildcard(self, ctx):
        raise NotImplementedError

    def visitMultiple_compound_wildcard(self, ctx):
        raise NotImplementedError
