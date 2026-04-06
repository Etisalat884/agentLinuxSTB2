*** Settings ***
Library           Video_metrics_robot.py
Library           BuiltIn
Library           Collections
Library           OperatingSystem

*** Variables ***
${video_port}     /dev/video2
${duration}       1
${trigger_id}     1234

*** Test Cases ***
TC_001_VQ_ANALYSIS
    ${results}=    CALCULATE VIDEO QUALITY    ${video_port}    ${duration}    ${trigger_id}
    Log To Console    Average Quality Score: ${results}
    EVALUATE VIDEO QUALITY STATUS    ${results}

*** Keywords ***
CALCULATE VIDEO QUALITY
    [Arguments]    ${video_port}    ${duration}    ${trigger_id}
    ${all_results}=    Create List
    ${total_score}=    Set Variable    0.0
    FOR    ${index}    IN RANGE    5
        ${result}=    video_metrics    ${video_port}    ${duration}    ${trigger_id}
        Log To Console    ${result}
        Append To List    ${all_results}    ${result}
        ${score}=    Get From Dictionary    ${result}    Quality_Score
        ${total_score}=    Evaluate    ${total_score} + ${score}
    END
    ${average}=    Evaluate    ${total_score} / 5
    ${average}=    Evaluate    round(${average}, 2)
    RETURN    ${average}

EVALUATE VIDEO QUALITY STATUS
    [Arguments]    ${score}
    ${score}=    Convert To Number    ${score}
    Run Keyword If    ${score} >= 80    Log To Console    Video quality is EXCELLENT
    ...    ELSE IF    ${score} >= 60    Log To Console    Video quality is GOOD
    ...    ELSE IF    ${score} >= 40    Log To Console    Video quality is AVERAGE
    ...    ELSE IF    ${score} >= 30    Log To Console    Video quality is POOR
    ...    ELSE    Fail    Video quality is BAD — Test Failed
