	FUNCTION TRAPZ1(X,Y,N)
	REAL X(N),Y(N)
	TRAPZ1=0.
	IF (N.LE.1) RETURN
	DO J=2,N
	TRAPZ1= TRAPZ1 + ABS(X(J)-X(J-1))*(Y(J)+Y(J-1))/2.
	ENDDO
	RETURN
	END
