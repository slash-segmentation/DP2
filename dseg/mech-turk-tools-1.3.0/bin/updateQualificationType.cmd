@echo off
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

:START
if "%MTURK_CMD_HOME%" == "" goto HOME_MISSING
call "%MTURK_CMD_HOME%\bin\invoke" UpdateQualificationType %*
GOTO DONE

:HOME_MISSING
echo MTURK_CMD_HOME is not set.  Defaulting to %CD%\..
set MTURK_CMD_HOME=%CD%\..
GOTO START

:DONE
if "%MTURK_TERMINATE_CMD%" == "on" exit %ERRORLEVEL%
exit /B %ERRORLEVEL%
