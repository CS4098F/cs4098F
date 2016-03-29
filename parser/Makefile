all:
	happy -gca ParPML.y
	alex -g LexPML.x
	ghc --make PMLparser.hs -o Pmlxml

clean:
	-rm -f *.log *.aux *.hi *.o *.dvi

distclean: clean
	-rm -f DocPML.* LexPML.* ParPML.* LayoutPML.* SkelPML.* PrintPML.* TestPML.* AbsPML.* TestPML ErrM.* SharedString.* ComposOp.* PML.dtd XMLPML.* Makefile*
	

