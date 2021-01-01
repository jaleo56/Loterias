
'''
Created on 17/12/2020

@author: jaleo
'''

import os
#import xlwings as xw
#from InfoLoteriasFromWeb import getGanadoraFromWeb, getPremiosFromWeb
#from InfoLoteriasToExcel import setGanadoraToExcel, setPremiosToExcel
from random import randrange


class BomboNumeros:

    def __init_(self, tLoteria, nApuestas):
        self.numerosJugados = list[]
        self.numerosPares = list[]
        self.numerosImpares = list[]

        if tLoteria = "PRIMITIVA":
            self.nMayor = 49
            self.nsCombinacion = 6
            self.nEstrellas = 0
        else:
            self.nMayor = 50
            self.nsCombinacion = 5
            self.nEstrellas = 12

        numerosJugados = [x + 1 for x in range(nMayor)]
        numerosPares = [x + 1 for x in range(nMayor) if x % 2 != 0]
        numerosImpares = [x + 1 for x in range(nMayor) if x % 2 == 0]


    def getNumeroAzar():
        return numerosJugados.pop(randrange(len(numerosJugados)))


    def getNumeroPar():
        return numerosPares.pop(randrange(len(numerosPares)))


    def getNumeroImpar():
        return numerosImpares.pop(randrange(len(numerosImpares)))




def ObtenerCombinaciones(juego):

    if juego == "PRIMITIVA":
        juegoRes = "lottoses"
        juegoPre = "lottoes"
    elif juego == "EUROMILLONES":
        juegoRes = "euromillonariases"
        juegoPre = "euromillonariaes"
    else:
        juegoRes = "quinises"
        juegoPre = "quinies"

    print ("passa por 1")

    jornadaId, jornadaDate, numeros = getGanadoraFromWeb(juego=juegoRes, year="2020")

    setGanadoraToExcel(jornadaId, jornadaDate, numeros)

    premios = getPremiosFromWeb(juego=juegoPre, jornadaId=jornadaId)

    setPremiosToExcel(premios)


if __name__ == "__main__":
    ObtenerCombinaciones("EUROMILLONES")


    def iterRows(df):
        count = 0
        for x, row in df.iterrows():
            # print ('Index:', x)
            # print (row)
            aset = set(row)
            print(aset)
            count += 1
            if count == 3: break


    def iterCols(df):
        count = 0
        for x, col in df.iteritems():
            print('Index:', x)
            print(col.head)
            count += 1
            if count == 3: break


    'Marcar numeros aleatorios en GRAELLA
    For i = 1 To NUMEROS_JUGADOS
        For j = 1 To 10
            For k = 1 To 5
                numero = ActiveSheet.Range(CELL_GRAELLA).OFFSET(j - 1, k - 1).value
                If NUMEROS(i) = numero Then
                    ActiveSheet.Range(CELL_GRAELLA).OFFSET(j - 1, k - 1).Font.color = vbRed
                    ActiveSheet.Range(CELL_GRAELLA).OFFSET(j - 1, k - 1).Font.Bold = True2
                    GoTo end_of_for
                End If
            Next k
        Next j
end_of_for:
    Next i

End Sub



Private Sub ObtenerNumerosIntervalos()
    Dim NUMEROS(5), numero, firstN, endN, nCol, nRow As Integer

    'Obtener numeros apuesta AL AZAR
    For i = 1 To CNT_INTERVALOS
        j = 999
        Do Until j <> 999
            numero = CInt(Int((10 * Rnd())))
            For j = 1 To i - 1
                If numero = NUMEROS(j) Then
                    j = 999
                    Exit For
                End If
            Next j
        Loop
        NUMEROS(i) = numero
    Next i

    'Marcar numeros aleatorios en GRAELLA
    For i = 1 To CNT_INTERVALOS
        If NUMEROS(i) = 0 Then
            firstN = 1
            endN = 5
        ElseIf NUMEROS(i) = 1 Then
            firstN = 6
            endN = 10
        ElseIf NUMEROS(i) = 2 Then
            firstN = 11
            endN = 15
        ElseIf NUMEROS(i) = 3 Then
            firstN = 16
            endN = 20
        ElseIf NUMEROS(i) = 4 Then
            firstN = 21
            endN = 25
        ElseIf NUMEROS(i) = 5 Then
            firstN = 26
            endN = 30
        ElseIf NUMEROS(i) = 6 Then
            firstN = 31
            endN = 35
        ElseIf NUMEROS(i) = 7 Then
            firstN = 36
            endN = 40
        ElseIf NUMEROS(i) = 8 Then
            firstN = 41
            endN = 45
        ElseIf NUMEROS(i) = 9 Then
            firstN = 46
            endN = NUMERO_MAYOR
        End If
        For nCol = 1 To 5
            For nRow = 1 To 10
                numero = ActiveSheet.Range(CELL_GRAELLA).OFFSET(nRow - 1, nCol - 1).value
                If numero >= firstN And numero <= endN Then
                    ActiveSheet.Range(CELL_GRAELLA).OFFSET(nRow - 1, nCol - 1).Font.color = vbRed
                    ActiveSheet.Range(CELL_GRAELLA).OFFSET(nRow - 1, nCol - 1).Font.Bold = True
                ElseIf numero > endN Then
                    GoTo end_of_for
                End If
            Next nRow
        Next nCol
end_of_for:
    Next i

End Sub


Public OPCION_SELECCION, CELL_NUMEROS, CELL_COMBINACIONES, CELL_GANADORA, CELL_GRAELLA, CELL_ACIERTOS, LOTERIA, _
    CELL_JORNADA, CELL_FECHA, CELL_PREMIOS, HOJA_COMBINACION As String
Public NUMEROS_JUGADOS, NUMERO_APUESTAS, NUMEROS_SORTEO, NUMERO_MAYOR, CNT_INTERVALOS As Integer
Public COLOR_NUMEROS As Variant

' -------------------------------------HOJA WORKING -----------------------------------------------
' -------------------------------------HOJA WORKING -----------------------------------------------
' -------------------------------------HOJA WORKING -----------------------------------------------
' -------------------------------------HOJA WORKING -----------------------------------------------


Sub CombinarTodosNumeros()

    Application.ScreenUpdating = False


    'Borrar resultados anteriores
    Call LimpiarPagina("CLEAN_COMBINATIONS")
    Call LimpiarPagina("SELECTION_NUMBERS")

    'Obtener GANADORA y PREMIOS
    RunPython ("import CombinarTodosNumeros as ctn; ctn.CombinarTodosNumeros")

    Application.ScreenUpdating = True

    Range("B1").Select

End Sub


Private Sub LimpiarPagina(ByVal opcion As String)

    'Restaurar números y fondo GRAELLA
    If opcion = "ALL" Or opcion = "SELECTION_NUMBERS" Then
        'Restaurar GRAELLA Primitva
        [O9:S18].Interior.ColorIndex = 0
        [O9:S18].Font.color = vbBlack
        [O9:S18].Font.Bold = False

        'Restaurar GRAELLA Euromillon
        [O22:S31].Interior.ColorIndex = 0
        [O22:S31].Font.color = vbBlack
        [O22:S31].Font.Bold = False
    End If

    If opcion = "ALL" Or opcion = "CLEAN_INTERIOR_COMBINATIONS" Then
        'Restaurar valor y fondo NUMEROS
        [D9:D55].Interior.ColorIndex = 0

        'Restaurar valor y fondo COMBINACIONES
        [F9:M200].Interior.ColorIndex = 0
    End If

    If opcion = "ALL" Or opcion = "CLEAN_COMBINATIONS" Then
        'Restaurar valor y fondo NUMEROS
        [D9:D55].ClearContents
        [D9:D55].Interior.ColorIndex = 0

        'Restaurar valor y fondo COMBINACIONES
        [F9:M200].ClearContents
        [F9:M200].Interior.ColorIndex = 0
    End If

    If opcion = "ALL" Or opcion = "CLEAN_GANADORA_Y_PREMIOS" Then
        'Restaurar valores y fondo GANADORA
        [F6:M6].ClearContents
        [F6:M6].Interior.ColorIndex = 0

        'Restaurar PREMIOS
        [V6:X18].ClearContents
        [V6:X18].Interior.ColorIndex = 0
    End If

End Sub


' -------------------------------------END HOJA WORKING -------------------------------------------
' -------------------------------------END HOJA WORKING -------------------------------------------
' -------------------------------------END HOJA WORKING -------------------------------------------
' -------------------------------------END HOJA WORKING -------------------------------------------




Sub Limpiar()
    Application.ScreenUpdating = False

    'Iniciar constantes
    Call IniciarConstantes

    'Borrar resultados anteriores
    Call LimpiarPagina("ALL")

    Range("B1").Select
    Application.ScreenUpdating = True
End Sub

Sub Seleccionar()
    Application.ScreenUpdating = False

    'Iniciar constantes
    Call IniciarConstantes

    'Limpiar numeros seleccionados en GRAELLA
    Call LimpiarPagina("SELECTION_NUMBERS")

    If OPCION_SELECCION = "AZAR" Then
        Call ObtenerNumerosAzar
    ElseIf OPCION_SELECCION = "INTERVALOS" Then
        Call ObtenerNumerosIntervalos
    ElseIf OPCION_SELECCION = "IMPARES" Then
        Call ObtenerNumerosImpares
    ElseIf OPCION_SELECCION = "PERIFERIA" Then
        Call ObtenerNumerosPeriferia
    ElseIf OPCION_SELECCION = "PATRONES" Then
            Call ObtenerNumerosPatrones
    End If

    Range("B1").Select
    Application.ScreenUpdating = True
End Sub

Sub Combinar()
    Dim numero As Integer
    Dim v() As Variant
    ReDim v(1 To 2)

    'Iniciar constantes
    Call IniciarConstantes

    'Borrar resultados anteriores
    Call LimpiarPagina("CLEAN_COMBINATIONS")

    'Obtener números apuestas a partir de la GRAELLA
    i = 0
    For c = 1 To 5
        For f = 1 To 10
            If (ActiveSheet.Range(CELL_GRAELLA).OFFSET(f - 1, c - 1).Font.color = COLOR_NUMEROS Or _
               ActiveSheet.Range(CELL_GRAELLA).OFFSET(f - 1, c - 1).Font.color = vbGreen) And _
               Not (LOTERIA = "PRIMITIVA" And f = 1 And c = 1) Then
                i = i + 1
                numero = ActiveSheet.Range(CELL_GRAELLA).OFFSET(f - 1, c - 1).value
                ActiveSheet.Range(CELL_NUMEROS).OFFSET(i - 1, 0).value = numero
            End If
        Next f
    Next c

    'Obtener combinaciones apuestas según fórmula
    For nFila = 1 To NUMERO_APUESTAS
        For nCol = 1 To NUMEROS_SORTEO
            orden = CInt(ActiveWorkbook.Sheets(HOJA_COMBINACION).Range("A1").OFFSET(nFila - 1, nCol - 1).value)
            ActiveSheet.Range(CELL_COMBINACIONES).OFFSET(nFila - 1, nCol - 1).value = ActiveSheet.Range(CELL_NUMEROS).OFFSET(orden - 1, 0).value
        Next nCol
    Next nFila

    'Obtener estrellas Euromillones apuestas
    If LOTERIA = "EUROMILLONES" Then
        For nFila = 1 To NUMERO_APUESTAS
            v = ObtenerEstrellas
            For nCol = 6 To 7
                ActiveSheet.Range(CELL_COMBINACIONES).OFFSET(nFila - 1, nCol - 1).value = v(nCol - 5)
            Next nCol
        Next nFila
    End If

    Range("B1").Select

End Sub

Sub ObtenerGanadoraEuromillones()

    Dim nFila As Integer
    Dim a As String

    nFila = CInt([A25].value)
    Sheets("working").Range("F6:J6") = Sheets("Euromillones").Range("B" & nFila & ":" & "F" & nFila).value
    Sheets("working").Range("L6:M6") = Sheets("Euromillones").Range("G" & nFila & ":" & "H" & nFila).value
    a = "B" & nFila & ":" & "I" & nFila

End Sub





Sub Combinar_todos()

    Dim numero, apuesta As Integer
    Dim Apuestas(10, 5) As Integer
    Dim swapuesta As Boolean

    Dim v() As Variant
    'ReDim v(1 To 2)

    'Iniciar constantes
    Call IniciarConstantes

    'Borrar resultados anteriores
    Call LimpiarPagina("CLEAN_COMBINATIONS")
    Call LimpiarPagina("SELECTION_NUMBERS")

    NUMERO_APUESTAS = 10

    'Recorrer números de la GRAELLA
    i = 0
    For c = 1 To 5
        For f = 1 To 10
            i = i + 1
            'Obtener siguiente numero graela
            numero = ActiveSheet.Range(CELL_GRAELLA).OFFSET(f - 1, c - 1).value

            'Publicar en excel el numero obtenido
            ActiveSheet.Range(CELL_NUMEROS).OFFSET(i - 1, 0).value = numero

            'Obtener apuesta libre: de 1 a 10
            apuesta = CInt(Int((NUMERO_APUESTAS * Rnd()) + 1))
            swapuesta = False
            Do Until (swapuesta = True)
                For a = 1 To 5                          '5 numeros por apuesta
                    If Apuestas(apuesta - 1, a - 1) = 0 Then
                        Apuestas(apuesta - 1, a - 1) = numero
                        swapuesta = True
                        Exit Do
                    End If
                Next a
                apuesta = apuesta + 1
                apuesta = apuesta Mod NUMERO_APUESTAS
                If apuesta = 0 Then apuesta = NUMERO_APUESTAS
            Loop

        Next f
    Next c

    'Publicar apuestas en excel
    For nFila = 1 To NUMERO_APUESTAS
        For nCol = 1 To 5
            ActiveSheet.Range(CELL_COMBINACIONES).OFFSET(nFila - 1, nCol - 1).value = Apuestas(nFila - 1, nCol - 1)
        Next nCol
    Next nFila

    'Obtener estrellas Euromillones apuestas
    If LOTERIA = "EUROMILLONES" Then
        v = ObtenerEstrellas_todos
        For nFila = 1 To NUMERO_APUESTAS
            For nCol = 6 To 7
                Range(CELL_COMBINACIONES).Cells(nFila, nCol).value = v(nFila, nCol - 5)
            Next nCol
        Next nFila
    End If

    Range("B1").Select

End Sub


Sub GanadoraYPremiosLoterias()
    Dim juego As String

    Application.ScreenUpdating = False


    'Borrar resultados anteriores
    Call LimpiarPagina("CLEAN_GANADORA_Y_PREMIOS")

    'Obtener GANADORA y PREMIOS
    RunPython ("import GanadoraYPremiosLoterias as gyp; gyp.GanadoraYPremiosLoterias")

    Application.ScreenUpdating = True

    Range("B1").Select

End Sub


Sub Comprobar()
    Dim acertado As Boolean
    Dim ganadora(1 To 8) As Integer
    Dim color As Integer

    'Iniciar constantes
    Call IniciarConstantes

    'Borrar resultados anteriores
    Call LimpiarPagina("CLEAN_INTERIOR_COMBINATIONS")
    Call LimpiarPagina("SELECTION_NUMBERS")


    'Obtener gadanadora
     For g = 1 To 8
        If [F6].Cells(1, g) <> "" Then
            ganadora(g) = CInt([F6].Cells(1, g).value)
        Else
            ganadora(g) = 0
        End If
    Next g


    ' Marcar ganadora en GRAELLA
    For g = 1 To 8
        If g <= NUMEROS_SORTEO Then color = 4 Else color = 6
        For j = 1 To 5
            For f = 1 To 10
                numero = Range(CELL_GRAELLA).Cells(f, j).value
                If numero = ganadora(g) Then
                    If (Range(CELL_GRAELLA).Cells(f, j).Font.color = COLOR_NUMEROS Or _
                        Range(CELL_GRAELLA).Cells(f, j).Font.color = vbGreen) Then
                        Range(CELL_GRAELLA).Cells(f, j).Interior.ColorIndex = color
                    Else
                        Range(CELL_GRAELLA).Cells(f, j).Interior.ColorIndex = color
                    End If
                    Exit For
                End If
            Next f
        Next j
    Next g


    ' Marcar ganadora en NUMEROS JUGADOS
    For g = 1 To 8
        For n = 1 To 50     'NUMEROS_JUGADOS
            num_jugado = CInt([D9].Cells(n, 1).value)
            If num_jugado = ganadora(g) Then
                If g <= NUMEROS_SORTEO Then color = 4 Else color = 6
                [D9].Cells(n, 1).Interior.ColorIndex = color
                [F6].Cells(1, g).Interior.ColorIndex = color
                Exit For
            Else
                [F6].Cells(1, g).Interior.ColorIndex = color
            End If
        Next n
    Next g

  'Marcar numeros acertados
    For a = 1 To NUMERO_APUESTAS
        nAciertos = 0
        'Marcar numeros premiados
        For n = 1 To NUMEROS_SORTEO
            If [F9].Cells(a, n) <> "" Then
                num_jugado = CInt([F9].Cells(a, n).value)
                For g = 1 To NUMEROS_SORTEO
                    If num_jugado = ganadora(g) Then
                        nAciertos = nAciertos + 1
                        [F9].Cells(a, n).Interior.ColorIndex = 4
                        Exit For
                    End If
                Next g
            End If
        Next n

        'Estrellas Euromillones
        nEstrellas = 0
        For n = 6 To 7
            If [F9].Cells(a, n) <> "" Then
                num_jugado = CInt([F9].Cells(a, n).value)
                For g = 7 To 8
                    If num_jugado = ganadora(g) Then
                        nEstrellas = nEstrellas + 1
                        [F9].Cells(a, n).Interior.ColorIndex = 6
                        Exit For
                    End If
                Next g
            End If
        Next n

        'publicar aciertos
        [M9].Cells(a, 1).value = nAciertos & "-" & nEstrellas
        [M9].Cells(a, 1).Font.color = vbRed
        [M9].Cells(a, 1).Font.Bold = True
        If nAciertos >= 2 Or nEstrellas > 1 Then
            [M9].Cells(a, 1).Interior.ColorIndex = 6
        End If
    Next a

    Range("B1").Select

End Sub
Public Sub Simular()
   Application.ScreenUpdating = False

    'Iniciar CONSTANTES globales del sistema
    Call IniciarConstantes

    'Borrar resultados anteriores
    Call LimpiarPagina("CLEAN_GANADORA_Y_PREMIOS")

    NUMERO_APUESTAS = ActiveWorkbook.Sheets("2013-a-2015").Range("A3").value

    Application.ScreenUpdating = True

    Range("B1").Select
End Sub

Private Sub IniciarConstantes()
    CNT_INTERVALOS = 5
    OPCION_SELECCION = ActiveSheet.Range("Q3").value
    CELL_NUMEROS = "D9"
    CELL_COMBINACIONES = "F9"
    CELL_GANADORA = "F6"
    CELL_ACIERTOS = "M9"
    CELL_JORNADA = "W3"
    CELL_FECHA = "W4"
    CELL_PREMIOS = "V6"

    If ActiveSheet.Range("J3").value = "R" Then
        COLOR_NUMEROS = vbRed
    Else
        COLOR_NUMEROS = vbBlack
    End If

    HOJA_COMBINACION = ActiveSheet.Range("F3").value
    If Left(HOJA_COMBINACION, 1) = "P" Then
        LOTERIA = "PRIMITIVA"
        CELL_GRAELLA = "O9"
        NUMEROS_SORTEO = 6
        NUMERO_MAYOR = 49
    Else
        LOTERIA = "EUROMILLONES"
        CELL_GRAELLA = "O22"
        NUMEROS_SORTEO = 5
        NUMERO_MAYOR = 50
    End If

    NUMEROS_JUGADOS = Mid(HOJA_COMBINACION, 2, 2) 'ActiveSheet.Range(CELL_NUMEROS).CurrentRegion.Rows.Count - 1
    NUMERO_APUESTAS = ActiveWorkbook.Sheets(HOJA_COMBINACION).Range("A1").CurrentRegion.Rows.Count
End Sub

Private Sub ObtenerNumerosAzar()
    Dim NUMEROS(50), numero As Integer

    'Obtener numeros apuesta AL AZAR
    For i = 1 To NUMEROS_JUGADOS
        j = 999
        Do Until j <> 999
            numero = CInt(Int((NUMERO_MAYOR * Rnd()) + 1))
            For j = 1 To i - 1
                If numero = NUMEROS(j) Then
                    j = 999
                    Exit For
                End If
            Next j
        Loop
        NUMEROS(i) = numero
    Next i

    'Marcar numeros aleatorios en GRAELLA
    For i = 1 To NUMEROS_JUGADOS
        For j = 1 To 10
            For k = 1 To 5
                numero = ActiveSheet.Range(CELL_GRAELLA).OFFSET(j - 1, k - 1).value
                If NUMEROS(i) = numero Then
                    ActiveSheet.Range(CELL_GRAELLA).OFFSET(j - 1, k - 1).Font.color = vbRed
                    ActiveSheet.Range(CELL_GRAELLA).OFFSET(j - 1, k - 1).Font.Bold = True2
                    GoTo end_of_for
                End If
            Next k
        Next j
end_of_for:
    Next i

End Sub

Private Sub ObtenerNumerosPeriferia()
    Dim numero As Integer

    'Seleccionar numeros periferia en GRAELLA
    For num = 1 To NUMEROS_JUGADOS
        For nRow = 1 To 10
            For nCol = 1 To 5
                If nRow = 1 Or nRow = 10 Or nCol = 1 Or nCol = 5 Then
                    ActiveSheet.Range(CELL_GRAELLA).OFFSET(nRow - 1, nCol - 1).Font.color = vbRed
                    ActiveSheet.Range(CELL_GRAELLA).OFFSET(nRow - 1, nCol - 1).Font.Bold = True
                End If
            Next nCol
        Next nRow
    Next num

End Sub

Private Sub ObtenerNumerosImpares()
    Dim numero As Integer

    'Marcar numeros impares en GRAELLA
    For i = 1 To NUMEROS_JUGADOS
        For j = 1 To 10
            For k = 1 To 5
                numero = ActiveSheet.Range(CELL_GRAELLA).OFFSET(j - 1, k - 1).value
                If numero Mod 2 <> 0 Then
                    ActiveSheet.Range(CELL_GRAELLA).OFFSET(j - 1, k - 1).Font.color = vbRed
                    ActiveSheet.Range(CELL_GRAELLA).OFFSET(j - 1, k - 1).Font.Bold = True
                End If
            Next k
        Next j
    Next i

End Sub

Private Sub ObtenerNumerosIntervalos()
    Dim NUMEROS(5), numero, firstN, endN, nCol, nRow As Integer

    'Obtener numeros apuesta AL AZAR
    For i = 1 To CNT_INTERVALOS
        j = 999
        Do Until j <> 999
            numero = CInt(Int((10 * Rnd())))
            For j = 1 To i - 1
                If numero = NUMEROS(j) Then
                    j = 999
                    Exit For
                End If
            Next j
        Loop
        NUMEROS(i) = numero
    Next i

    'Marcar numeros aleatorios en GRAELLA
    For i = 1 To CNT_INTERVALOS
        If NUMEROS(i) = 0 Then
            firstN = 1
            endN = 5
        ElseIf NUMEROS(i) = 1 Then
            firstN = 6
            endN = 10
        ElseIf NUMEROS(i) = 2 Then
            firstN = 11
            endN = 15
        ElseIf NUMEROS(i) = 3 Then
            firstN = 16
            endN = 20
        ElseIf NUMEROS(i) = 4 Then
            firstN = 21
            endN = 25
        ElseIf NUMEROS(i) = 5 Then
            firstN = 26
            endN = 30
        ElseIf NUMEROS(i) = 6 Then
            firstN = 31
            endN = 35
        ElseIf NUMEROS(i) = 7 Then
            firstN = 36
            endN = 40
        ElseIf NUMEROS(i) = 8 Then
            firstN = 41
            endN = 45
        ElseIf NUMEROS(i) = 9 Then
            firstN = 46
            endN = NUMERO_MAYOR
        End If
        For nCol = 1 To 5
            For nRow = 1 To 10
                numero = ActiveSheet.Range(CELL_GRAELLA).OFFSET(nRow - 1, nCol - 1).value
                If numero >= firstN And numero <= endN Then
                    ActiveSheet.Range(CELL_GRAELLA).OFFSET(nRow - 1, nCol - 1).Font.color = vbRed
                    ActiveSheet.Range(CELL_GRAELLA).OFFSET(nRow - 1, nCol - 1).Font.Bold = True
                ElseIf numero > endN Then
                    GoTo end_of_for
                End If
            Next nRow
        Next nCol
end_of_for:
    Next i

End Sub


Private Sub LimpiarPagina(ByVal opcion As String)

    'Restaurar números y fondo GRAELLA
    If opcion = "ALL" Or opcion = "SELECTION_NUMBERS" Then
        'Restaurar GRAELLA Primitva
        Range("O9:S18").Interior.ColorIndex = 0
        Range("O9:S18").Font.color = vbBlack
        Range("O9:S18").Font.Bold = False

        'Restaurar GRAELLA Euromillon
        Range("O22:S31").Interior.ColorIndex = 0
        Range("O22:S31").Font.color = vbBlack
        Range("O22:S31").Font.Bold = False
    End If

      If opcion = "ALL" Or opcion = "CLEAN_INTERIOR_COMBINATIONS" Then
        'Restaurar valor y fondo NUMEROS
        Range("D9:D55").Interior.ColorIndex = 0

        'Restaurar valor y fondo COMBINACIONES
        Range("F9:M200").Interior.ColorIndex = 0
    End If

    If opcion = "ALL" Or opcion = "CLEAN_COMBINATIONS" Then
        'Restaurar valor y fondo NUMEROS
        Range("D9:D55").ClearContents
        Range("D9:D55").Interior.ColorIndex = 0

        'Restaurar valor y fondo COMBINACIONES
        Range("F9:M200").ClearContents
        Range("F9:M200").Interior.ColorIndex = 0
    End If

    If opcion = "ALL" Or opcion = "CLEAN_GANADORA_Y_PREMIOS" Then
        'Restaurar valores y fondo GANADORA
        Range("F6:M6").ClearContents
        Range("F6:M6").Interior.ColorIndex = 0

        'Restaurar PREMIOS
        Range("V6:X18").ClearContents
        Range("V6:X18").Interior.ColorIndex = 0
    End If

End Sub

Function ObtenerEstrellas()
        Dim v() As Variant
        Dim n As Integer
        ReDim v(1 To 2)

        i = 0
        Do Until i >= 2
            n = CInt(Int((11 * Rnd()) + 1))
            If n <> v(1) Then
                i = i + 1
                v(i) = n
            End If
        Loop

        If v(2) < v(1) Then
            n = v(1)
            v(1) = v(2)
            v(2) = n
        End If

        ObtenerEstrellas = v

End Function
Function ObtenerEstrellas_todos()
        Dim Apuestas(1 To 10, 1 To 2) As Variant
        Dim n, apuesta As Integer

        For i = 1 To 20
            n = i Mod 12
            If n = 0 Then n = 12
            'Obtener apuesta libre: de 1 a 10
            swapuesta = False
            apuesta = CInt(Int((NUMERO_APUESTAS * Rnd()) + 1))
            Do Until (swapuesta = True)
                For a = 1 To 2                          '5 numeros por apuesta
                    If Apuestas(apuesta, a) = 0 Then
                        Apuestas(apuesta, a) = n
                        swapuesta = True
                        Exit Do
                    End If
                Next a
                apuesta = apuesta + 1
                apuesta = apuesta Mod NUMERO_APUESTAS
                If apuesta = 0 Then apuesta = NUMERO_APUESTAS
            Loop
        Next i

        ObtenerEstrellas_todos = Apuestas

End Function

Sub Combinaciones5()
    Dim sortida As String

    i = 0

    For n1 = 0 To 9
        For n2 = n1 + 1 To 9
            For n3 = n2 + 1 To 9
                For n4 = n3 + 1 To 9
                    For n5 = n4 + 1 To 9
                        i = i + 1
                        sortida = CStr(n1) + CStr(n2) + CStr(n3) + CStr(n4) + CStr(n5)
                        ActiveWorkbook.Sheets("Combis").Range("A1").OFFSET(i - 1, 0).value = sortida
                    Next n5
                Next n4
            Next n3
        Next n2
    Next n1

End Sub

Sub Buscar()
    Dim lookupvalue As Variant, value As Variant, lookupRange As Range
    r = ActiveSheet.Range("B1:B34")

    nFilas = ActiveSheet.Range("A1").CurrentRegion.Rows.Count - 1
    For i = 1 To nFilas
        value = ActiveSheet.Range("A1").OFFSET(i - 1, 0).value
        On Error Resume Next
        lookupvalue = Application.VLookup(value, r, 1, False)
        If Not IsError(lookupvalue) Then
            ActiveSheet.Range.OFFSET(i - 1, 0).Interior.ColorIndex = 12
        End If
    Next i

End Sub

Private Sub ObtenerNumerosPatrones()
    Dim patron As String, x As Integer

    patron = [Q4].value
    x = InputBox("Ingresar numero linea ganadora")

End Sub
