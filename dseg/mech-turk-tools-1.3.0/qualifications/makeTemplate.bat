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

REM You must supply at least one parameter
IF (%1)==() GOTO TOO_FEW_PARAMS
IF EXIST %1 GOTO DIR_ALREADY_EXISTS

mkdir %1
copy ..\etc\templates\qualifications\template.question %1\%1.question
copy ..\etc\templates\qualifications\template.answer %1\%1.answer
copy ..\etc\templates\qualifications\template.properties %1\%1.properties

REM create the createQualification.cmd file for DOS
echo @echo off >> %1\createQualification.cmd
echo cd ..\.. >> %1\createQualification.cmd
echo cd bin >> %1\createQualification.cmd
echo call createQualificationType %%1 %%2 %%3 %%4 %%5 %%6 %%7 %%8 %%9 -question ..\qualifications\%1\%1.question -properties ..\qualifications\%1\%1.properties -answer ..\qualifications\%1\%1.answer  >> %1\createQualification.cmd
echo cd .. >> %1\createQualification.cmd
echo cd qualifications\%1 >> %1\createQualification.cmd

REM create the updateQualification.cmd file for DOS
echo @echo off >> %1\updateQualification.cmd
echo cd ..\.. >> %1\updateQualification.cmd
echo cd bin >> %1\updateQualification.cmd
echo call updateQualificationType %%1 %%2 %%3 %%4 %%5 %%6 %%7 %%8 %%9 -qualtypeid [put your qualification id here] -question ..\qualifications\%1\%1.question -properties ..\qualifications\%1\%1.properties -answer ..\qualifications\%1\%1.answer >> %1\updateQualification.cmd
echo cd .. >> %1\updateQualification.cmd
echo cd qualifications\%1 >> %1\updateQualification.cmd

REM create the deactivateQualification.cmd file for DOS
echo @echo off >> %1\deactivateQualification.cmd
echo cd ..\.. >> %1\deactivateQualification.cmd
echo cd bin >> %1\deactivateQualification.cmd
echo call updateQualificationType  %%1 %%2 %%3 %%4 %%5 %%6 %%7 %%8 %%9 -qualtypeid [put your qualification id here] -status Inactive >> %1\deactivateQualification.cmd
echo cd .. >> %1\deactivateQualification.cmd
echo cd qualifications\%1 >> %1\deactivateQualification.cmd

GOTO END

:TOO_FEW_PARAMS
echo Usage: makeTemplate [name of template folder to automatically generate]
GOTO :END

:DIR_ALREADY_EXISTS
echo Directory '%1' already exists
GOTO :END

:END
