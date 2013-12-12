rem @echo off
rem
rem Copyright 2008 Amazon Technologies, Inc.
rem 
rem Licensed under the Amazon Software License (the "License");
rem you may not use this file except in compliance with the License.
rem You may obtain a copy of the License at:
rem 
rem http://aws.amazon.com/asl
rem 
rem This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES
rem OR CONDITIONS OF ANY KIND, either express or implied. See the
rem License for the specific language governing permissions and
rem limitations under the License.
rem 
rem


:START

if "%MTURK_CMD_HOME%" == "" goto MTURK_CMD_HOME_MISSING

REM Remove this line if you wish to NOT use the built-in JRE

if "%JAVA_HOME%" == "" goto CHECK_JRE_FOLDER

setlocal EnableDelayedExpansion

REM If a classpath exists preserve it
SET CP=%CLASSPATH%

REM Brute force
REM Amazon Mechanical Turk Command Line Tools Jars
SET CP=%CP%;%MTURK_CMD_HOME%\lib\mturk\aws-mturk-clt.jar
SET CP=%CP%;%MTURK_CMD_HOME%\lib\third-party\jakarta-commons-cli\commons-cli-1.0.jar

REM Location of log4j.properties 
SET CP=%CP%;%MTURK_CMD_HOME%\etc

REM Support running commands from repository build environment
FOR /R "%CD%\..\build\lib" %%I IN (*.JAR) DO ( SET CP=!CP!;%%I )

REM Amazon Mechanical Turk Java SDK and third party Jars
FOR /R "%CD%\..\lib" %%I IN (*.JAR) DO ( SET CP=!CP!;%%I )

REM Grab the class name
SET CMD=%1

REM Check if class name is fully qualified, otherwise prepend default
echo %1 | findstr "\." > nul
if %errorlevel% equ 1 (
   SET CMD=com.amazonaws.mturk.cmd.%CMD%
) 

REM SHIFT doesn't affect %* so we need this clunky hack
SET ARGV=%2
SHIFT
SHIFT
:ARGV_LOOP
IF (%1) == () GOTO ARGV_DONE
SET ARGV=%ARGV% %1
SHIFT
GOTO ARGV_LOOP
:ARGV_DONE

"%JAVA_HOME:"=%\bin\java" %MTURK_JVM_ARGS% -classpath "%CP%" %CMD% %ARGV%
goto DONE

:CHECK_JRE_FOLDER
IF NOT EXIST "%CD%\..\jre1.5.0_06" goto JAVA_HOME_MISSING
echo Defaulting to %CD%\..\jre1.5.0_06
SET JAVA_HOME=%CD%\..\jre1.5.0_06
GOTO START

:JAVA_HOME_MISSING
echo JAVA_HOME is not set. 
GOTO DONE

:MTURK_CMD_HOME_MISSING
echo MTURK_CMD_HOME is not set.  Defaulting to ..\%CD%
SET MTURK_CMD_HOME=..\%CD%
GOTO START


:DONE
endlocal
exit /B %ERRORLEVEL%
