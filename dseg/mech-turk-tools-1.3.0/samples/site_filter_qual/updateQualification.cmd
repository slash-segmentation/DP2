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
rem

 
cd ..\..
cd bin 
call updateQualificationType %1 %2 %3 %4 %5 %6 %7 %8 %9 -sandbox -input ..\samples\site_filter_qual\site_filter_qual.properties.success -question ..\samples\site_filter_qual\site_filter_qual.question -properties ..\samples\site_filter_qual\site_filter_qual.properties -answer ..\samples\site_filter_qual\site_filter_qual.answer 
cd .. 
cd samples\site_filter_qual 
