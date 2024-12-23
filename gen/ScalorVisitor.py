# Generated from /home/kostiantyn/PycharmProjects/Scalor/antlr/Scalor.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .ScalorParser import ScalorParser
else:
    from ScalorParser import ScalorParser

# This class defines a complete generic visitor for a parse tree produced by ScalorParser.

class ScalorVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by ScalorParser#program.
    def visitProgram(self, ctx:ScalorParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScalorParser#declSection.
    def visitDeclSection(self, ctx:ScalorParser.DeclSectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScalorParser#declarList.
    def visitDeclarList(self, ctx:ScalorParser.DeclarListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScalorParser#declaration.
    def visitDeclaration(self, ctx:ScalorParser.DeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScalorParser#varDecl.
    def visitVarDecl(self, ctx:ScalorParser.VarDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScalorParser#valDecl.
    def visitValDecl(self, ctx:ScalorParser.ValDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScalorParser#type.
    def visitType(self, ctx:ScalorParser.TypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScalorParser#doSection.
    def visitDoSection(self, ctx:ScalorParser.DoSectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScalorParser#statementList.
    def visitStatementList(self, ctx:ScalorParser.StatementListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScalorParser#statement.
    def visitStatement(self, ctx:ScalorParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScalorParser#assign.
    def visitAssign(self, ctx:ScalorParser.AssignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScalorParser#ifStatement.
    def visitIfStatement(self, ctx:ScalorParser.IfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScalorParser#whileStatement.
    def visitWhileStatement(self, ctx:ScalorParser.WhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScalorParser#printStatement.
    def visitPrintStatement(self, ctx:ScalorParser.PrintStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScalorParser#inputStatement.
    def visitInputStatement(self, ctx:ScalorParser.InputStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScalorParser#expression.
    def visitExpression(self, ctx:ScalorParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScalorParser#boolExpr.
    def visitBoolExpr(self, ctx:ScalorParser.BoolExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScalorParser#arithmExpression.
    def visitArithmExpression(self, ctx:ScalorParser.ArithmExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScalorParser#power.
    def visitPower(self, ctx:ScalorParser.PowerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScalorParser#term.
    def visitTerm(self, ctx:ScalorParser.TermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScalorParser#factor.
    def visitFactor(self, ctx:ScalorParser.FactorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScalorParser#concatExpression.
    def visitConcatExpression(self, ctx:ScalorParser.ConcatExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScalorParser#doBlock.
    def visitDoBlock(self, ctx:ScalorParser.DoBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScalorParser#constant.
    def visitConstant(self, ctx:ScalorParser.ConstantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScalorParser#relOp.
    def visitRelOp(self, ctx:ScalorParser.RelOpContext):
        return self.visitChildren(ctx)



del ScalorParser