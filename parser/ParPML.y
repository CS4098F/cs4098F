-- This Happy file was machine-generated by the BNF converter
{
{-# OPTIONS_GHC -fno-warn-incomplete-patterns -fno-warn-overlapping-patterns #-}
module ParPML where
import AbsPML
import LexPML
import ErrM

}

%name pPML_PROCESS PML_PROCESS
-- no lexer declaration
%monad { Err } { thenM } { returnM }
%tokentype {Token}
%token
  '!' { PT _ (TS _ 1) }
  '!=' { PT _ (TS _ 2) }
  '&&' { PT _ (TS _ 3) }
  '(' { PT _ (TS _ 4) }
  ')' { PT _ (TS _ 5) }
  '.' { PT _ (TS _ 6) }
  '<' { PT _ (TS _ 7) }
  '<=' { PT _ (TS _ 8) }
  '==' { PT _ (TS _ 9) }
  '>' { PT _ (TS _ 10) }
  '>=' { PT _ (TS _ 11) }
  'action' { PT _ (TS _ 12) }
  'agent' { PT _ (TS _ 13) }
  'branch' { PT _ (TS _ 14) }
  'executable' { PT _ (TS _ 15) }
  'iteration' { PT _ (TS _ 16) }
  'manual' { PT _ (TS _ 17) }
  'process' { PT _ (TS _ 18) }
  'provides' { PT _ (TS _ 19) }
  'requires' { PT _ (TS _ 20) }
  'script' { PT _ (TS _ 21) }
  'selection' { PT _ (TS _ 22) }
  'sequence' { PT _ (TS _ 23) }
  'task' { PT _ (TS _ 24) }
  'tool' { PT _ (TS _ 25) }
  '{' { PT _ (TS _ 26) }
  '||' { PT _ (TS _ 27) }
  '}' { PT _ (TS _ 28) }

L_STRING { PT _ (T_STRING $$) }
L_ID { PT _ (T_ID $$) }
L_NUMBER { PT _ (T_NUMBER $$) }


%%

STRING    :: { STRING} : L_STRING { STRING ($1)}
ID    :: { ID} : L_ID { ID ($1)}
NUMBER    :: { NUMBER} : L_NUMBER { NUMBER ($1)}

PML_PROCESS :: { PML_PROCESS }
PML_PROCESS : 'process' ID '{' ListPRIM '}' { Process $2 (reverse $4) }
ListPRIM :: { [PRIM] }
ListPRIM : {- empty -} { [] } | ListPRIM PRIM { flip (:) $1 $2 }
PRIM :: { PRIM }
PRIM : 'branch' OPTNM '{' ListPRIM '}' { PrimBr $2 (reverse $4) }
     | 'selection' OPTNM '{' ListPRIM '}' { PrimSeln $2 (reverse $4) }
     | 'iteration' OPTNM '{' ListPRIM '}' { PrimIter $2 (reverse $4) }
     | 'sequence' OPTNM '{' ListPRIM '}' { PrimSeq $2 (reverse $4) }
     | 'task' OPTNM '{' ListPRIM '}' { PrimTask $2 (reverse $4) }
     | 'action' ID OPTYP '{' ListSPEC '}' { PrimAct $2 $3 (reverse $5) }
OPTNM :: { OPTNM }
OPTNM : {- empty -} { OpNmNull } | ID { OpNmId $1 }
OPTYP :: { OPTYP }
OPTYP : {- empty -} { OptNull }
      | 'manual' { OptMan }
      | 'executable' { OptExec }
ListSPEC :: { [SPEC] }
ListSPEC : {- empty -} { [] } | ListSPEC SPEC { flip (:) $1 $2 }
SPEC :: { SPEC }
SPEC : 'provides' '{' EXPR '}' { SpecProv $3 }
     | 'requires' '{' EXPR '}' { SpecReqs $3 }
     | 'agent' '{' EXPR '}' { SpecAgent $3 }
     | 'script' '{' STRING '}' { SpecScript $3 }
     | 'tool' '{' STRING '}' { SpecTool $3 }
EXPR :: { EXPR }
EXPR : EXPR2 { $1 }
EXPR2 :: { EXPR }
EXPR2 : EXPR3 { $1 } | EXPR2 '||' EXPR3 { DisjExpr $1 $3 }
EXPR3 :: { EXPR }
EXPR3 : EXPR4 { $1 } | EXPR3 '&&' EXPR4 { ConjExpr $1 $3 }
EXPR4 :: { EXPR }
EXPR4 : STRING { Str $1 }
      | EXPR5 { $1 }
      | VALEXPR '==' VALEXPR { RelEq $1 $3 }
      | VALEXPR '!=' VALEXPR { RelNe $1 $3 }
      | VALEXPR '<' VALEXPR { RelLt $1 $3 }
      | VALEXPR '>' VALEXPR { RelGt $1 $3 }
      | VALEXPR '<=' VALEXPR { RelLe $1 $3 }
      | VALEXPR '>=' VALEXPR { RelGe $1 $3 }
      | VAREXPR '==' VAREXPR { RelVeq $1 $3 }
      | VAREXPR '!=' VAREXPR { RelVne $1 $3 }
EXPR5 :: { EXPR }
EXPR5 : VAREXPR { PrimVar $1 }
      | ATTREXPR { PrimAttr $1 }
      | '!' EXPR5 { PrimNot $2 }
      | '(' EXPR ')' { $2 }
VAREXPR :: { VAREXPR }
VAREXPR : ID { VarId $1 }
        | '(' ID ')' { VarPar $2 }
        | '(' ID ')' VAREXPR { VarMore $2 $4 }
ATTREXPR :: { ATTREXPR }
ATTREXPR : VAREXPR '.' ID { Attr $1 $3 }
VALEXPR :: { VALEXPR }
VALEXPR : ATTREXPR { ValAttr $1 }
        | STRING { ValString $1 }
        | NUMBER { ValNum $1 }
{

returnM :: a -> Err a
returnM = return

thenM :: Err a -> (a -> Err b) -> Err b
thenM = (>>=)

happyError :: [Token] -> Err a
happyError ts =
  Bad $ "syntax error at " ++ tokenPos ts ++ 
  case ts of
    [] -> []
    [Err _] -> " due to lexer error"
    _ -> " before " ++ unwords (map (id . prToken) (take 4 ts))

myLexer = tokens
}

