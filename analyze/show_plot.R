library(tcltk)
if(!require('graphics')) {
  install.packages('graphics')
  library('graphics')
}

FIGURE_ID = 0

figure <- function(name=NULL) {
    if (is.null(name)) {
        name = sprintf("figure %d", FIGURE_ID)
        FIGURE_ID <<- FIGURE_ID + 1
    }
    system_info <- Sys.info()
    system_name <- system_info["sysname"]
    if (system_name == "Windows") {
        windows.options(title = name)
        fig <- windows()
    } else {
        X11.options(title = name)
        fig <- X11()
    }
    return(fig)
}

show <- function() {
    prompt  <- "Hit spacebar to close plots."
    extra   <- "Stay strong, working in 'R' is not forever.\nYou can do it! :D"
    capture <- tk_messageBox(message = prompt, detail = extra)
}

