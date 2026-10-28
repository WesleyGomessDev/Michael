# Michael

@echo off
REM ======================================================================
REM  backup_usuario.bat
REM  Backup do usuario logado para C:\temp\Backup_%USERNAME%
REM  - Somente CMD e comandos nativos (robocopy, copy, tasklist, timeout)
REM  - Nao precisa de administrador e nao instala nada
REM  - Nao altera nem apaga os arquivos originais
REM ======================================================================

REM Quando o script chama a si mesmo (copia em segundo plano), vai para :Worker
if /i "%~1"=="/worker" goto :Worker

setlocal EnableExtensions EnableDelayedExpansion
title Backup de %USERNAME%

set "SELF=%~f0"
for /f %%a in ('copy /Z "%~f0" nul') do set "CR=%%a"

set "DEST=C:\temp\Backup_%USERNAME%"
set "LOG=C:\temp\backup_%USERNAME%.log"
set "ERROS=0"

if not exist "C:\temp\" mkdir "C:\temp" >nul 2>&1
if not exist "%DEST%\" mkdir "%DEST%" >nul 2>&1
if not exist "%DEST%\" goto :ErroDestino

set "T0=!time!"
2>nul > "%LOG%" echo ===== Backup de %USERNAME% iniciado em %date% %time% =====

echo.
call :Log "Usuario....: %USERNAME%"
call :Log "Computador.: %COMPUTERNAME%"
call :Log "Destino....: %DEST%"
call :Log "Log........: %LOG%"
call :AvisarSeExcelAberto
echo.

REM ===== 1) Favoritos do Chrome e do Edge (arquivo Bookmarks de cada perfil) =====
call :Log "--- Favoritos do navegador ---"
call :CopiarFavoritos "%LOCALAPPDATA%\Google\Chrome\User Data" "Chrome"
call :CopiarFavoritos "%LOCALAPPDATA%\Microsoft\Edge\User Data" "Edge"

REM ===== 2) BcpConfig (aceita "Agencia" com ou sem acento) =====
call :Log "--- BcpConfig ---"
set "BCP=%APPDATA%\Agencia Estado\Broadcast\BcpConfig"
if not exist "!BCP!\" for /d %%D in ("%APPDATA%\Ag?ncia Estado") do set "BCP=%%~fD\Broadcast\BcpConfig"
call :CopiarPasta "!BCP!" "%DEST%\BcpConfig" "BcpConfig" "" "/E"

REM ===== 3) Excel: XLSTART, Personal.xlsb, Add-ins e arquivos .xlsb =====
call :Log "--- Excel ---"
set "XLDIR=%APPDATA%\Microsoft\Excel"
call :CopiarPasta "!XLDIR!\XLSTART" "%DEST%\Excel\XLSTART" "Excel XLSTART" "" "/E"
call :VerificarPersonal
call :CopiarPasta "%APPDATA%\Microsoft\AddIns" "%DEST%\Excel\AddIns" "Excel Add-ins" "" "/E"
call :CopiarPasta "!XLDIR!" "%DEST%\Excel\XLSB" "Arquivos .xlsb da pasta do Excel" "*.xlsb" ""

REM ===== 4) Acesso Rapido (somente o arquivo de itens fixados) =====
call :Log "--- Acesso Rapido ---"
call :CopiarArquivo "%APPDATA%\Microsoft\Windows\Recent\AutomaticDestinations\f01b4d95cf55d32a.automaticDestinations-ms" "%DEST%\AcessoRapido" "Acesso Rapido"

REM ===== Resumo final =====
call :CalcularTempo "!T0!" "!time!"
echo.
call :Log "===== Concluido. Tempo total: !DURACAO! ====="
call :Log "Itens com erro: !ERROS!"
call :Log "Backup em: %DEST%"
call :Log "Log em...: %LOG%"
echo.
echo Pressione qualquer tecla para fechar...
pause >nul
endlocal
exit /b 0

REM ======================================================================
REM                              SUB-ROTINAS
REM ======================================================================

:Log
REM Mostra na tela e grava no log com a hora
set "MSG=%~1"
set "HORA=!time: =0!"
echo !MSG!
2>nul >> "%LOG%" echo [!HORA:~0,8!] !MSG!
goto :eof

:AvisarSeExcelAberto
tasklist /fi "imagename eq excel.exe" /nh 2>nul | find /i "excel.exe" >nul 2>&1
if errorlevel 1 goto :eof
call :Log "[AVISO] O Excel esta aberto. O Personal.xlsb pode estar em uso e falhar na copia. Se der erro, feche o Excel e rode de novo."
goto :eof

:VerificarPersonal
set "PERSONAL=%APPDATA%\Microsoft\Excel\XLSTART\Personal.xlsb"
if exist "!PERSONAL!" goto :VP_Sim
call :Log "[INFO] Personal.xlsb nao encontrado em XLSTART (normal se nao houver macros pessoais)."
goto :eof
:VP_Sim
call :Log "[INFO] Personal.xlsb encontrado em XLSTART (incluido na copia do XLSTART)."
goto :eof

:CopiarFavoritos
REM %1 = pasta "User Data" do navegador | %2 = nome do navegador
if not exist "%~1\" goto :CF_Ignorado
for /d %%P in ("%~1\Default" "%~1\Profile *") do call :CopiarBookmarks "%%~fP" "%~2" "%%~nxP"
goto :eof
:CF_Ignorado
call :Log "[IGNORADO] Navegador %~2 nao encontrado."
goto :eof

:CopiarBookmarks
REM %1 = pasta do perfil | %2 = navegador | %3 = nome do perfil
call :CopiarArquivo "%~1\Bookmarks" "%DEST%\Favoritos_%~2\%~3" "Favoritos %~2 [%~3]"
goto :eof

:CopiarArquivo
REM %1 = arquivo de origem | %2 = pasta de destino | %3 = nome para exibir
if not exist "%~1" goto :CA_Ignorado
if not exist "%~2\" mkdir "%~2" >nul 2>&1
copy /Y "%~1" "%~2\" >nul 2>&1
if errorlevel 1 goto :CA_Erro
call :Log "[OK] %~3 copiado."
goto :eof
:CA_Erro
set /a "ERROS+=1"
call :Log "[ERRO] %~3: nao foi possivel copiar (arquivo em uso ou sem permissao): %~1"
goto :eof
:CA_Ignorado
call :Log "[IGNORADO] %~3 nao encontrado: %~1"
goto :eof

:CopiarPasta
REM %1 = origem | %2 = destino | %3 = nome | %4 = mascara (opcional) | %5 = opcoes (opcional)
set "ITEM=%~3"
if not exist "%~1\" goto :CP_Ignorado
call :Log "Copiando !ITEM! ..."
set "FLAG=%TEMP%\bkflag_%RANDOM%%RANDOM%.tmp"
del /q "!FLAG!" "!FLAG!.run" >nul 2>&1
set "TI=!time!"
start "" /b cmd /c call "!SELF!" /worker "%~1" "%~2" "!FLAG!" "%LOG%" "%~4" "%~5"
call :Aguardar
goto :eof
:CP_Ignorado
call :Log "[IGNORADO] !ITEM! nao encontrado: %~1"
goto :eof

:Aguardar
REM Mostra o tempo decorrido ao vivo ate o robocopy terminar
set /a "ESPERA=0"
:AG_Loop
timeout /t 1 /nobreak >nul
set /a "ESPERA+=1"
call :CalcularTempo "!TI!" "!time!"
<nul set /p "=   Tempo decorrido: !DURACAO!        !CR!"
if exist "!FLAG!" goto :AG_Fim
if !ESPERA! equ 8 if not exist "!FLAG!.run" goto :AG_NaoIniciou
if !ESPERA! lss 14400 goto :AG_Loop
echo.
set /a "ERROS+=1"
call :Log "[ERRO] Tempo limite excedido ao copiar !ITEM!."
goto :eof
:AG_NaoIniciou
echo.
set /a "ERROS+=1"
call :Log "[ERRO] Nao foi possivel iniciar a copia de !ITEM!."
goto :eof
:AG_Fim
call :CalcularTempo "!TI!" "!time!"
echo.
set "RC="
set /p RC=<"!FLAG!"
del /q "!FLAG!" "!FLAG!.run" >nul 2>&1
if not defined RC set "RC=16"
set /a "RCN=RC" 2>nul
if !RCN! geq 8 goto :AG_Erro
if !RCN! equ 0 goto :AG_Nada
call :Log "[OK] !ITEM! copiado em !DURACAO! (robocopy codigo !RCN!)."
goto :eof
:AG_Nada
call :Log "[OK] !ITEM!: nenhum arquivo novo ou alterado (!DURACAO!)."
goto :eof
:AG_Erro
set /a "ERROS+=1"
call :Log "[ERRO] !ITEM!: nem todos os arquivos foram copiados (robocopy codigo !RCN!, !DURACAO!)."
call :Log "       Causas comuns: arquivo em uso (feche Excel e navegadores) ou sem permissao de leitura."
call :Log "       Detalhes de cada arquivo estao no log."
goto :eof

:CalcularTempo
REM %1 = hora inicial | %2 = hora final (formato do %time%). Trata a virada de meia-noite.
call :ParaCentesimos "%~1" CS_INI
call :ParaCentesimos "%~2" CS_FIM
set /a "CS_DIF=CS_FIM-CS_INI"
if !CS_DIF! lss 0 set /a "CS_DIF+=8640000"
set /a "TH=CS_DIF/360000, TM=(CS_DIF%%360000)/6000, TS=(CS_DIF%%6000)/100"
set "DURACAO=!TH!h !TM!min !TS!s"
goto :eof

:ParaCentesimos
REM Converte HH:MM:SS,cc em centesimos de segundo (aceita hora com 1 digito e evita erro de octal)
for /f "tokens=1-4 delims=:,. " %%a in ("%~1") do (
    set "_h=0%%a"
    set "_m=0%%b"
    set "_s=0%%c"
    set "_c=0%%d"
)
set "_h=!_h:~-2!"
set "_m=!_m:~-2!"
set "_s=!_s:~-2!"
set "_c=!_c:~-2!"
set /a "%~2=(1!_h!-100)*360000+(1!_m!-100)*6000+(1!_s!-100)*100+(1!_c!-100)"
goto :eof

:ErroDestino
echo.
echo ERRO: nao foi possivel criar a pasta "%DEST%".
echo Verifique se voce tem permissao de escrita em C:\ e se ha espaco em disco.
echo.
pause
exit /b 1

:Worker
REM Executado em segundo plano: %2=origem %3=destino %4=arquivo-sinal %5=log %6=mascara %7=opcoes
> "%~4.run" echo 1
robocopy "%~2" "%~3" %~6 %~7 /R:1 /W:1 /XJ /NP /NDL /NJH /LOG+:"%~5" >nul 2>&1
> "%~4.w" echo %errorlevel%
ren "%~4.w" "%~nx4"
exit /b
