*** Settings ***
Library    BuiltIn
Library    OperatingSystem
Library    Collections
*** Variables ***
${ZAP_LIMIT}     3    # 3 milliseconds
@{ZAP_TIMES}     # List to store each zap time in ms


*** Test Cases ***
Measure Multiple Zaps On STB
  ${total_zaps}=    Set Variable    5
  FOR    ${i}    IN RANGE    ${total_zaps}
      ${zap_time}=    Zap And Measure Time
      Append To List    ${ZAP_TIMES}    ${zap_time}
      Log To Console    Zap ${i+1}: ${zap_time} ms
      Should Be True    ${zap_time} < ${ZAP_LIMIT}    Zap ${i+1} took too long!
  END
  ${total_time}=    Evaluate    sum(${ZAP_TIMES})
  Log To Console    Total zaps: ${total_zaps}
  Log To Console    Total time taken: ${total_time} ms
  
*** Keywords ***
Zap And Measure Time
  ${start}=    Evaluate    __import__('time').time()
  Press Down Key
  ${end}=      Evaluate    __import__('time').time()
  ${elapsed}=  Evaluate    round((${end} - ${start}) * 1000, 3)    # convert to milliseconds
  [Return]    ${elapsed}
  
Press Down Key
  # Replace with actual zap logic for STB
  Log    Sending DOWN key
  Sleep    0.002    # Simulate 2 milliseconds delay