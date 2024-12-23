# Generated from /home/kostiantyn/PycharmProjects/Scalor/antlr/Scalor.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .ScalorParser import ScalorParser
else:
    from ScalorParser import ScalorParser

# This class defines a complete listener for a parse tree produced by ScalorParser.
class ScalorListener(ParseTreeListener):

    # Enter a parse tree produced by ScalorParser#program.
    def enterProgram(self, ctx:ScalorParser.ProgramContext):
        pass

    # Exit a parse tree produced by ScalorParser#program.
    def exitProgram(self, ctx:ScalorParser.ProgramContext):
        pass


    # Enter a parse tree produced by ScalorParser#declSection.
    def enterDeclSection(self, ctx:ScalorParser.DeclSectionContext):
        pass

    # Exit a parse tree produced by ScalorParser#declSection.
    def exitDeclSection(self, ctx:ScalorParser.DeclSectionContext):
        pass


    # Enter a parse tree produced by ScalorParser#declarList.
    def enterDeclarList(self, ctx:ScalorParser.DeclarListContext):
        pass

    # Exit a parse tree produced by ScalorParser#declarList.
    def exitDeclarList(self, ctx:ScalorParser.DeclarListContext):
        pass


    # Enter a parse tree produced by ScalorParser#declaration.
    def enterDeclaration(self, ctx:ScalorParser.DeclarationContext):
        pass

    # Exit a parse tree produced by ScalorParser#declaration.
    def exitDeclaration(self, ctx:ScalorParser.DeclarationContext):
        pass


    # Enter a parse tree produced by ScalorParser#varDecl.
    def enterVarDecl(self, ctx:ScalorParser.VarDeclContext):
        pass

    # Exit a parse tree produced by ScalorParser#varDecl.
    def exitVarDecl(self, ctx:ScalorParser.VarDeclContext):
        pass


    # Enter a parse tree produced by ScalorParser#valDecl.
    def enterValDecl(self, ctx:ScalorParser.ValDeclContext):
        pass

    # Exit a parse tree produced by ScalorParser#valDecl.
    def exitValDecl(self, ctx:ScalorParser.ValDeclContext):
        pass


    # Enter a parse tree produced by ScalorParser#type.
    def enterType(self, ctx:ScalorParser.TypeContext):
        pass

    # Exit a parse tree produced by ScalorParser#type.
    def exitType(self, ctx:ScalorParser.TypeContext):
        pass


    # Enter a parse tree produced by ScalorParser#doSection.
    def enterDoSection(self, ctx:ScalorParser.DoSectionContext):
        pass

    # Exit a parse tree produced by ScalorParser#doSection.
    def exitDoSection(self, ctx:ScalorParser.DoSectionContext):
        pass


    # Enter a parse tree produced by ScalorParser#statementList.
    def enterStatementList(self, ctx:ScalorParser.StatementListContext):
        pass

    # Exit a parse tree produced by ScalorParser#statementList.
    def exitStatementList(self, ctx:ScalorParser.StatementListContext):
        pass


    # Enter a parse tree produced by ScalorParser#statement.
    def enterStatement(self, ctx:ScalorParser.StatementContext):
        pass

    # Exit a parse tree produced by ScalorParser#statement.
    def exitStatement(self, ctx:ScalorParser.StatementContext):
        pass


    # Enter a parse tree produced by ScalorParser#assign.
    def enterAssign(self, ctx:ScalorParser.AssignContext):
        pass

    # Exit a parse tree produced by ScalorParser#assign.
    def exitAssign(self, ctx:ScalorParser.AssignContext):
        pass


    # Enter a parse tree produced by ScalorParser#ifStatement.
    def enterIfStatement(self, ctx:ScalorParser.IfStatementContext):
        pass

    # Exit a parse tree produced by ScalorParser#ifStatement.
    def exitIfStatement(self, ctx:ScalorParser.IfStatementContext):
        pass


    # Enter a parse tree produced by ScalorParser#whileStatement.
    def enterWhileStatement(self, ctx:ScalorParser.WhileStatementContext):
        pass

    # Exit a parse tree produced by ScalorParser#whileStatement.
    def exitWhileStatement(self, ctx:ScalorParser.WhileStatementContext):
        pass


    # Enter a parse tree produced by ScalorParser#printStatement.
    def enterPrintStatement(self, ctx:ScalorParser.PrintStatementContext):
        pass

    # Exit a parse tree produced by ScalorParser#printStatement.
    def exitPrintStatement(self, ctx:ScalorParser.PrintStatementContext):
        pass


    # Enter a parse tree produced by ScalorParser#inputStatement.
    def enterInputStatement(self, ctx:ScalorParser.InputStatementContext):
        pass

    # Exit a parse tree produced by ScalorParser#inputStatement.
    def exitInputStatement(self, ctx:ScalorParser.InputStatementContext):
        pass


    # Enter a parse tree produced by ScalorParser#expression.
    def enterExpression(self, ctx:ScalorParser.ExpressionContext):
        pass

    # Exit a parse tree produced by ScalorParser#expression.
    def exitExpression(self, ctx:ScalorParser.ExpressionContext):
        pass


    # Enter a parse tree produced by ScalorParser#boolExpr.
    def enterBoolExpr(self, ctx:ScalorParser.BoolExprContext):
        pass

    # Exit a parse tree produced by ScalorParser#boolExpr.
    def exitBoolExpr(self, ctx:ScalorParser.BoolExprContext):
        pass


    # Enter a parse tree produced by ScalorParser#arithmExpression.
    def enterArithmExpression(self, ctx:ScalorParser.ArithmExpressionContext):
        pass

    # Exit a parse tree produced by ScalorParser#arithmExpression.
    def exitArithmExpression(self, ctx:ScalorParser.ArithmExpressionContext):
        pass


    # Enter a parse tree produced by ScalorParser#power.
    def enterPower(self, ctx:ScalorParser.PowerContext):
        pass

    # Exit a parse tree produced by ScalorParser#power.
    def exitPower(self, ctx:ScalorParser.PowerContext):
        pass


    # Enter a parse tree produced by ScalorParser#term.
    def enterTerm(self, ctx:ScalorParser.TermContext):
        pass

    # Exit a parse tree produced by ScalorParser#term.
    def exitTerm(self, ctx:ScalorParser.TermContext):
        pass


    # Enter a parse tree produced by ScalorParser#factor.
    def enterFactor(self, ctx:ScalorParser.FactorContext):
        pass

    # Exit a parse tree produced by ScalorParser#factor.
    def exitFactor(self, ctx:ScalorParser.FactorContext):
        pass


    # Enter a parse tree produced by ScalorParser#concatExpression.
    def enterConcatExpression(self, ctx:ScalorParser.ConcatExpressionContext):
        pass

    # Exit a parse tree produced by ScalorParser#concatExpression.
    def exitConcatExpression(self, ctx:ScalorParser.ConcatExpressionContext):
        pass


    # Enter a parse tree produced by ScalorParser#doBlock.
    def enterDoBlock(self, ctx:ScalorParser.DoBlockContext):
        pass

    # Exit a parse tree produced by ScalorParser#doBlock.
    def exitDoBlock(self, ctx:ScalorParser.DoBlockContext):
        pass


    # Enter a parse tree produced by ScalorParser#constant.
    def enterConstant(self, ctx:ScalorParser.ConstantContext):
        pass

    # Exit a parse tree produced by ScalorParser#constant.
    def exitConstant(self, ctx:ScalorParser.ConstantContext):
        pass


    # Enter a parse tree produced by ScalorParser#relOp.
    def enterRelOp(self, ctx:ScalorParser.RelOpContext):
        pass

    # Exit a parse tree produced by ScalorParser#relOp.
    def exitRelOp(self, ctx:ScalorParser.RelOpContext):
        pass



del ScalorParser