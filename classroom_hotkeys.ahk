#SingleInstance Force
SendMode Input
SetTitleMatchMode, 2

OpenInChrome(url) {
    if WinExist("ahk_exe chrome.exe") {
        WinActivate
        WinWaitActive, ahk_exe chrome.exe, , 2
        Run, chrome.exe --new-tab "%url%"
    } else {
        Run, chrome.exe "%url%"
    }
}

OpenYouTubeRandom() {
    queries := ["binaural beats", "deep focus music", "lofi work music", "ambient study music", "brown noise", "alpha waves focus"]
    Random, idx, 1, % queries.Length()
    x := queries[idx]
    y := StrReplace(x, " ", "+")
    z := "https://www.youtube.com/results?search_query=" . y
    OpenInChrome(z)

    WinWaitActive, ahk_exe chrome.exe, , 3
    Random, delay, 900, 1600
    Sleep, %delay%
    Send, {Tab 7}{Enter}
}

3::OpenInChrome("https://classroom.google.com/u/1/c/ODI0ODM4MzczODI0")
2::OpenInChrome("https://classroom.google.com/u/1/c/ODI0NTUzNjAzMzU2")
1::OpenInChrome("https://classroom.google.com/u/1/c/ODI1MDU1NTg4Mjk3")
4::OpenYouTubeRandom()
