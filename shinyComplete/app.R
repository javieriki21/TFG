library(shiny)
library(shinydashboard)
library(tidyverse)
library(plotly)
library(reshape2)
library(png)
library(grid)
library(magick)
library(extrafont)
library(jsonlite)
library("shiny")
library("shinythemes")
library(gridExtra)
library(grid)

##library(rsconnect)
##rsconnect::deployApp('path/to/your/app')


datosFunnelPuzzle <- read.csv("pruebaBinarioV2.csv", header = TRUE)
total_puzzles <- 30
datosFunnelUser <- read.csv("funnelOutput.csv", header = TRUE)
#datosFunnelUser<-datosFunnelUser%>% filter(level_puzzle != "SAND")
datosFunnelPuzzle$level_puzzle <- factor(datosFunnelPuzzle$level_puzzle, levels = c("Basic Puzzles", "Intermediate Puzzles","Advanced Puzzles")) ## En ese factor falta poner todos los niveles en el orden de la plataforma de los puzles 
datosFunnelPuzzle<-datosFunnelPuzzle%>% filter(level_puzzle != "SAND")

dfSequence <- read.csv("sequenceOutput.csv", header = TRUE)
dfActivity <- read.csv("activityOutput.csv", header = TRUE)
#dfActivity<-dfActivity%>% filter(level_puzzle != "SAND")
datosDiff <- read.csv("levelsOfDifficultyOutput.csv", header = TRUE)
seqWithinDf <- read.csv("seqWPOutput.csv", header = TRUE)
commonErrorsDf <- read.csv("commonOutput.csv", header = TRUE)
datosCompetencyELO<- read.csv("datosCompetencyELO_normalized.csv", header = TRUE)
datosDifficultyELO<- read.csv("datosDifficultyELO_normalized.csv", header = TRUE)
df_melted <- NULL
currentSeq<- NULL
dfCompetencyELO<-NULL

#Controls event click on funnel plot
event<- 0
#Controls student key to change plot
k <- NULL
kBetweenPuzzlesTask <- NULL

eventCompetency<-0
eventL<- 0
#Controls event click on sequenceBP plot
eventBetweenPuzzles<- 0
#Controls student key to change plot
kBetweenPuzzles <- NULL

seqWithinDf <- seqWithinDf %>% mutate(task_id = paste(task_id,  paste("-Attempt", n_attempt), sep = ""))

seqWithinDf$type <- factor(seqWithinDf$type, levels = c("ws-check_solution", "ws-create_shape", "ws-delete_shape", "ws-move_shape", "ws-rotate_shape", "ws-rotate_view", "ws-scale_shape", "ws-snapshot", "ws-start_level"), 
                           labels = c("submit", "create", "delete", "move", "rotate", "rotate_view", "scale", "snapshot", "start_level"))

seqWithinDf$shape_type <- factor(seqWithinDf$shape_type, levels = c("-", "1", "2", "3", "4", "5", "6"), 
                                 labels = c("-", "cube", "pyramid", "prism", "cylinder", "cone", "sphere"))

common_errors <- image_read("common_errors.png")
master_sol_img <- image_read("master_sol.png")
no_data <- image_read("nodata.png")
sphere <- image_read("shape_sphere.png")
cone <- image_read("shape_cone.png")
cube <- image_read("shape_cube.png")
ramp <- image_read("shape_prism.png")
pyramid <- image_read("shape_pyramid.png")
cylinder <- image_read("shape_cylinder.png")

create_sphere <- image_read("add_sphere.png")
create_cone <- image_read("add_cone.png")
create_cube <- image_read("add_cube.png")
create_cylinder <- image_read("add_cylinder.png")
create_prism <- image_read("add_prism.png")
create_pyramid <- image_read("add_pyramid.png")

delete_sphere <- image_read("delete_sphere.png")
delete_cone <- image_read("delete_cone.png")
delete_cube <- image_read("delete_cube.png")
delete_cylinder <- image_read("delete_cylinder.png")
delete_prism <- image_read("delete_prism.png")
delete_pyramid <- image_read("delete_pyramid.png")

scale_sphere <- image_read("scale_sphere.png")
scale_cone <- image_read("scale_cone.png")
scale_cube <- image_read("scale_cube.png")
scale_cylinder <- image_read("scale_cylinder.png")
scale_prism <- image_read("scale_prism.png")
scale_pyramid <- image_read("scale_pyramid.png")

move_sphere <- image_read("move_sphere.png")
move_cone <- image_read("move_cone.png")
move_cube <- image_read("move_cube.png")
move_cylinder <- image_read("move_cylinder.png")
move_prism <- image_read("move_prism.png")
move_pyramid <- image_read("move_pyramid.png")

rotate_sphere <- image_read("rotate_sphere.png")
rotate_cone <- image_read("rotate_cone.png")
rotate_cube <- image_read("rotate_cube.png")
rotate_cylinder <- image_read("rotate_cylinder.png")
rotate_prism <- image_read("rotate_prism.png")
rotate_pyramid <- image_read("rotate_pyramid.png")

submit_correct <- image_read("submit_correct.png")
submit_incorrect <- image_read("submit_incorrect.png")
snapshot <- image_read("snapshot.png")
rotate_view <- image_read("rotate_view.png")
pizarra <- image_read("pizarra.png")

userSelected <- "86eafa4b05f579291048d9f8e4e715fd"


dashboardSid<-dashboardSidebar(
  sidebarMenu(id = "menu",
    menuItem("Funnel", tabName = "dashboardFunnel", icon = icon("chart-pie")),
    menuItem("Sequence between Puzzles", tabName = "sequenceBP", icon = icon("ellipsis-h")),
    menuItem("Sequence within Puzzles", tabName = "sequenceWP", icon = icon("ellipsis-h")),
    menuItem("Common Errors", tabName = "common_err", icon = icon("times")),
    menuItem("Levels of Activity", tabName = "activity", icon = icon("chart-line")),
    menuItem("Levels of Difficulty", tabName = "difficulty", icon = icon("book")),
    menuItem("ELO-based learner", tabName = "dashboardELO", icon = icon("caret-square-down"),
             menuSubItem("User competency", tabName = "Subdashboardcompetency", icon = icon("user-graduate")),
             menuSubItem("Puzzle Difficulty", tabName = "SubdashboardELOdifficulty", icon = icon("pencil-alt")))
  )
) 


body <- dashboardBody(
  tabItems(
    tabItem(tabName = "dashboardFunnel",
            fluidRow(
              tabBox(
                # The id lets us use input$tabset1 on the server to find the current tab
                id = "tabset1",
                tabPanel("Funnel by Puzzle",
                         box(
                           selectizeInput(inputId = "groupPuzzle", label = "Choose a group",
                                          choices = unique(datosFunnelPuzzle$group), options = list(
                                            placeholder = 'Please select a group',
                                            onInitialize = I('function() { this.setValue(""); }')
                                          ),width = 1000), width = 1000,height = 100, offset = 5),box(plotlyOutput("funnelPuzzle", height = 900, width = 1000), width = 12, height = 950), width = 1000, height = 150,offset = 5),
                
                tabPanel("Funnel by User",
                         box(
                           selectizeInput(inputId = "groupUser", label = "Choose a group",
                                          choices = unique(datosFunnelUser$group), options = list(
                                            placeholder = 'Please select a group',
                                            onInitialize = I('function() { this.setValue(""); }')
                                          ), selected = "8cbfa61cb2b025b16b04a8e470422960",width = 1000),width = 1000,height = 100, offset = 5), box(plotlyOutput("funnelUser", height = 900, width = 1000), width = 12, height = 950),width = 1000,height = 150,offset = 5), height = 150, width = 1000
              )
            )
    ),
    
    
    tabItem(tabName = "Subdashboardcompetency",
            fluidRow(
              column (box(
                selectizeInput(inputId = "groupCompetency", label = "Choose a group",
                               choices = unique(datosCompetencyELO$group), options = list(
                                 placeholder = 'Please select a group',
                                 onInitialize = I('function() { this.setValue(""); }')
                               ))
              ), width = 12, offset = 3), column (box(plotlyOutput("competencyELO", height = 600, width = 1000), width = 12, height = 650), width = 12)
            )
    ),
    
    tabItem(tabName = "SubdashboardELOdifficulty",
            fluidRow(
              column (box(
                selectizeInput(inputId = "groupDifficulty", label = "Choose a group",
                               choices = unique(datosDifficultyELO$group), options = list(
                                 placeholder = 'Please select a group',
                                 onInitialize = I('function() { this.setValue(""); }')
                               ))
              ), width = 12, offset = 3), column (box(plotlyOutput("difficultyELO", height = 600, width = 1000), width = 12, height = 650), width = 12)
            )
    ),
    
    tabItem(tabName = "sequenceBP",
            fluidRow(column (box( selectizeInput(
              'groupDiff', "Choose a group - the group will be used to calculate the difficulty metric", unique(datosFunnelUser$group),
              options = list(
                placeholder = 'Please select a group',
                onInitialize = I('function() { this.setValue(""); }')
              )
            )), width = 12, box(selectizeInput(inputId = "user", label = "Choose a user",
                                               choices = unique(dfSequence$user), options = list(
                                                 placeholder = 'Please select a user',
                                                 onInitialize = I('function() { this.setValue(""); }')
                                               )))), column (box(plotlyOutput("sequenceBetweenPuzzles", height = 500, width = 1100), width = 12, height = 550), width = 12))),
    tabItem(tabName = "activity",
            fluidRow(column (box(selectizeInput(inputId = "groupLevels", label = "Choose a group",
                                                choices = unique(datosFunnelUser$group), options = list(
                                                  placeholder = 'Please select a group',
                                                  onInitialize = I('function() { this.setValue(""); }')
                                                ))), width = 12, box(
                                                  selectizeInput(inputId = "userLevel", label = "Choose a user",
                                                                 choices = unique(unique(dfActivity$user)), options = list(
                                                                   placeholder = 'Please select a user',
                                                                   onInitialize = I('function() { this.setValue(""); }')
                                                                 ))
                                                )),  column (box(plotlyOutput("levelsOfActivity", height = 600, width = 1000), width = 12, height = 650), width = 12)
            )
    ),
    tabItem(tabName = "sequenceWP",
            fluidRow(column (box(selectizeInput(inputId = "sequenceWPGroup", label = "Choose a group",
                                                choices = unique(seqWithinDf$group), options = list(
                                                  placeholder = 'Please select a group',
                                                  onInitialize = I('function() { this.setValue(""); }')
                                                ))), box(selectizeInput(inputId = "sequenceWPUser", label = "Choose a user",
                                                                 choices = unique(unique(seqWithinDf$user)), options = list(
                                                                   placeholder = 'Please select a user',
                                                                   onInitialize = I('function() { this.setValue(""); }')
                                                                 ))
                                                ), width = 12)), fluidRow(column(width = 12,
                                                  box(selectizeInput(inputId = "sequenceWPPuzzle", label = "Choose a puzzle",
                                                                 choices = unique(unique(seqWithinDf$task_id)), options = list(
                                                                   placeholder = 'Please select a puzzle',
                                                                   onInitialize = I('function() { this.setValue(""); }')
                                                                 )), width = 12)), width = 12),  fluidRow(column (plotOutput("sequenceWP", height = 800, width = 700), width = 12, align = "center")
                     )
    )
    , tabItem(tabName = "common_err",
             fluidRow(column (box(selectizeInput(inputId = "common_errGroup", label = "Choose a group",
                                                 choices = unique(commonErrorsDf$group_id), options = list(
                                                   placeholder = 'Please select a group',
                                                   onInitialize = I('function() { this.setValue(""); }')
                                                 ))), width = 12, box(
                                                   selectizeInput(inputId = "common_errPuzzle", label = "Choose a puzzle",
                                                                  choices = unique(unique(commonErrorsDf$task_id)), options = list(
                                                                    placeholder = 'Please select a puzzle',
                                                                    onInitialize = I('function() { this.setValue(""); }')
                                                                  )))),  fluidRow(column (align = "center", plotOutput("common_errPlot", height = 800, width = 700), width = 12))
             )
    ),
    tabItem(tabName = "difficulty",
            fluidRow(
              column (box(
                selectizeInput(inputId = "groupLevelsOfDifficulty", label = "Choose a group",
                               choices = unique(datosDiff$group), options = list(
                                 placeholder = 'Please select a group',
                                 onInitialize = I('function() { this.setValue(""); }')
                               ))
              ), width = 12, offset = 3), column (box(plotlyOutput("levelsOfDifficulty", height = 600, width = 1000), width = 12, height = 650), width = 12)
            )
    )

  )
)




ui <- dashboardPage(
  dashboardHeader(title = "Shadowspect Dashboard", titleWidth = 500),
  dashboardSid,
  body
  
)



server <- function(session,input, output) {
  
  ############################
  
  observe({
    

    if (nchar(input$groupLevels) < 1) {k <<- NULL}
    else {
      eL <<- event_data(
        
        event = "plotly_click",
        source = "L",
        session = session
      )

      new_valueL <- ifelse(is.null(eL),"0",(eL$pointNumber+1)) # 0 if no selection
      if(eventL!=new_valueL) {
        eventL <<- new_valueL 
        if(eventL !=0) {
         updateTabItems(session, "menu",
                         selected = "SubdashboardELOdifficulty")
          groupL=input$groupLevels
          updateSelectizeInput(session, "groupDifficulty", selected= groupL)
          
          
        }
      }else{}
      
    }
  })
  
  
  
  
  ############################
  
  
  observe({

    
    if (nchar(input$groupCompetency) < 1) {k <<- NULL}
    else {
      eC <<- event_data(
        
        event = "plotly_click",
        source = "C",
        session = session
      )
      sortUs <- sort(unique(dfCompetencyELO$user))[(eC$pointNumber + 1)]
      dfComp <- dfCompetencyELO[dfCompetencyELO$user==sortUs,]
      keyC <- unique(dfComp$userN)
      
      new_valueComp <- ifelse(is.null(eC),"0",(eC$pointNumber+1)) # 0 if no selection
      if(eventCompetency!=new_valueComp) {
        eventCompetency <<- new_valueComp 
        if(eventCompetency !=0) {
          updateTabItems(session, "menu",
                         selected = "activity")
          groupU = unique(datosCompetencyELO[datosCompetencyELO$user==keyC,]$group)
          updateSelectizeInput(session, "groupLevels", selected= groupU)
          selectComp=datosCompetencyELO %>% filter(group == groupU) %>% select(user)
          k <<- keyC
          updateSelectInput(session, "userLevel",choices = selectComp, selected = keyC)

        }
      }else{}
      
    }
  })

  
  ############################
  
  observe({
    selectClass = datosFunnelUser %>% filter(group == input$groupDiff) %>% select(user)
    updateSelectInput(session, "user","Select a user",choices = selectClass, selected = k)

    if (nchar(input$groupUser) < 1) {k <<- NULL}
    else {
      e <<- event_data(
        
        event = "plotly_click",
        source = "F",
        session = session
      )
      st <- sort(unique(df_melted$user))[(e$curveNumber + 1)]
      df_ch <- df_melted[df_melted$user==st,]
      key <- unique(df_ch$userN)
      
      new_value <- ifelse(is.null(e),"0",(e$curveNumber+1)) # 0 if no selection
      if(event!=new_value) {
        event <<- new_value 
        if(event !=0) {
          updateTabItems(session, "menu",
                         selected = "sequenceBP")
        groupUpdate = unique(datosFunnelUser[datosFunnelUser$user==key,]$group)
        updateSelectizeInput(session, "groupDiff", selected = groupUpdate)
        selectClass = datosFunnelUser %>% filter(group == groupUpdate) %>% select(user)
        k <<- key
        updateSelectInput(session, "user","Select a user",choices = selectClass, selected = key)
        #updateSelectInput(session, "user", selected = key)
        }
      }
      
    }
  })
  
  
  observe({
    selectPuzzle = seqWithinDf %>% filter(group_id == input$sequenceWPGroup)  %>% filter (user == input$sequenceWPUser) %>% select(task_id)
    updateSelectInput(session, "sequenceWPPuzzle","Select a puzzle",choices = selectPuzzle, selected = kBetweenPuzzlesTask)
  })
  
  
  
  observe({
    prevVal <- kBetweenPuzzles
    selectClassSequence = seqWithinDf %>% filter(group_id == input$sequenceWPGroup) %>% select(user)
    updateSelectInput(session, "sequenceWPUser","Select a user",choices = selectClassSequence, selected = kBetweenPuzzles)
    #kBetweenPuzzles <<- NULL
    #kBetweenPuzzlesTask <<- NULL
    
    if (nchar(input$user) < 1) {}
    else {
      eS <<- event_data(
        event = "plotly_click",
        source = "S",
        session = session
      )
        new_value <- ifelse(is.null(eS),"0",(eS$pointNumber+1)) # 0 if no selection
        if(eventBetweenPuzzles!=new_value) {
          eventBetweenPuzzles <<- new_value
          if(eventBetweenPuzzles !=0) {
            gr = input$groupDiff
            us = input$user
            nAttempt = eS$x
            updateTabItems(session, "menu",
                           selected = "sequenceWP")
            updateSelectizeInput(session, "sequenceWPGroup", selected = gr)
            
            namePuzzle = unique(currentSeq[currentSeq$sequence == nAttempt,]$task_id)
            at = paste("-Attempt", nAttempt, sep = " ")
            pD <- paste(namePuzzle, at, sep="")
            #print(currentSeq[currentSeq$n_attempt == nAttempt,])
            #print(pD)
            selectClassSequence = seqWithinDf %>% filter(group_id == input$sequenceWPGroup) %>% select(user)
            selectPuzzle = seqWithinDf %>% filter(group_id == input$sequenceWPGroup)  %>% filter (user == input$sequenceWPUser) %>% select(task_id)
            kBetweenPuzzles <<- us
            kBetweenPuzzlesTask <<- pD
            updateSelectInput(session, "sequenceWPUser",choices = selectClassSequence, selected = us)
            updateSelectInput(session, "sequenceWPPuzzle", choices = selectPuzzle, selected = pD)
          }
        }
      
    }
  })
  

  
  observe({
    selectTaskId= commonErrorsDf %>% filter(group_id == input$common_errGroup)  %>% select(task_id)
    updateSelectInput(session, "common_errPuzzle","Select a puzzle",choices = selectTaskId)
  })
  
  observe({
   
  })
  
  
  output$competencyELO <- renderPlotly({
    
    if (nchar(input$groupCompetency) < 1) {}
    else {
      dfCompetencyELO <- datosCompetencyELO%>% filter(group == input$groupCompetency)%>% mutate(competency = round(competency,2)) 
      dfCompetencyELO <- dfCompetencyELO %>% mutate(userN = user)
      dfCompetencyELO <<- dfCompetencyELO %>% melt(id.vars = c("user","userN"))
      #dfCompetencyELO <- dfCompetencyELO %>% rename(kc = Knowledge_Components)
      names(dfCompetencyELO)[which(names(dfCompetencyELO) == "kc")] <- "KC"
      actiCompetency <-ggplot(dfCompetencyELO, aes(x=user, y = competency, fill = KC)) +  geom_bar(stat='identity', position='stack') +  theme_minimal() +  theme(axis.text.x = element_text(angle = 90, size = 7),plot.title = element_text(hjust = 0.5)) +
        theme(legend.position = 'bottom') + labs(title ="Competency ELO", x = "", y = "Competency")
      ggplotly(actiCompetency, tooltip = c("x", "y"), source="C")
    }
  })
  
  output$funnelUser <- renderPlotly ({
    
    if (nchar(input$groupUser) < 1) {}
    else {
      df1 <- datosFunnelUser  %>% mutate(started = started/total_puzzles, create_shape = create_shape/total_puzzles, submitted = submitted/total_puzzles, completed = completed/total_puzzles) %>% filter(group == input$groupUser) %>% select(-task_id, -group)
      df1 <- df1 %>% mutate(userN = user)
      df_melted <<- df1 %>% melt(id.vars = c("user","userN"), measure.vars = c("started", "create_shape", "submitted", "completed"), variable.name = "funnel_state") %>% mutate(user = paste("Student",  as.numeric(user)))
     
      df_melted <<- df_melted %>% mutate(percentage = round(value * 100),2)
      ax <- list(
        title = "",
        zeroline = FALSE,
        showline = FALSE,
        showticklabels = FALSE,
        showgrid = FALSE
      )
      cont = 0
      nr = as.integer(length(unique(df_melted$user))/6)
      p.list = lapply(sort(unique(df_melted$user)), function(i) {
        df_use <- df_melted[df_melted$user==i,]
        funnel <- plot_ly(source = "F") 
        funnel <- funnel %>%
          add_trace(df_use,
                    type = "funnel",
                    y =  df_use$funnel_state,
                    x =  df_use$percentage, textinfo = "value"
                    ,marker = list(color = c("deepskyblue", "yellow", "red", "chartreuse"),
                                                          line = list(width = c(1,1,1,1), color = c("deepskyblue", "yellow", "red", "lightgreen"))),
                    connector = list(line = list(color = "royalblue", dash = "dot", width = 3)), name = unique(df_use$user))
        funnel <- funnel %>% add_annotations(
          text = ~unique(df_use$user),
          x = 0.5,
          y = 3.5,
          yref = "y",
          xref = "x",
          xanchor = "middle",
          yanchor = "top",
          showarrow = FALSE,
          font = list(size = 15)
        ) 
        
        if (cont%%as.integer(((length(unique(df_melted$user))/nr) + 1)) != 0) {
          funnel <- funnel %>% layout(yaxis = ax)
        }
        cont <<- cont + 1
        
        funnel
        
      })
      subplot(p.list, nrows = nr) %>% layout(showlegend = FALSE)
    }
    
  })
  
  output$funnelPuzzle <- renderPlotly ({
    
    if (nchar(input$groupPuzzle) < 1) {}
    else {
      
      datosFunnelPuzzle <- datosFunnelPuzzle %>% filter(group==input$groupPuzzle)
      total_students <- length(unique(datosFunnelPuzzle$user))
      
      datosFunnelPuzzle <- datosFunnelPuzzle %>% group_by(task_id,level_puzzle) %>% summarise(started = sum(started), create_shape = sum(create_shape), submitted = sum(submitted), completed = sum(completed)) %>% 
        mutate(started = started/total_students, create_shape = create_shape/total_students, submitted = submitted/total_students, completed = completed/total_students) # %>% filter(level_puzzle==input$level_puzzle)
      datos_melted <- datosFunnelPuzzle %>% melt(id.vars = c("task_id","level_puzzle"), measure.vars = c("started", "create_shape", "submitted", "completed"), value.name = "percentage", variable.name = "funnel_state")
      datos_melted$funnel_state <- factor(datos_melted$funnel_state, levels = c("started","create_shape","submitted", "completed"), labels = c("started","create_shape","submitted", "completed"))
      datos_melted <- datos_melted %>% mutate(percentage = round(percentage * 100),2)
      ax <- list(
        title = "",
        zeroline = FALSE,
        showline = FALSE,
        showticklabels = FALSE,
        showgrid = FALSE
      )
      
      cont1 = 0
      #nr2 = as.integer(length(unique(datos_melted$task_id))/6)
      if (length(unique(datos_melted$task_id)) == 30) {
        nr2 = 5
      } else {
        nr2 = 4
      }
      p.list = lapply(sort(unique(datos_melted$task_id)), function(i) {
        df_use <- datos_melted[datos_melted$task_id==i,]
        funnel <- plot_ly() 
        funnel <- funnel %>%
          add_trace(df_use,
                    type = "funnel",
                    y =  df_use$funnel_state,
                    x =  df_use$percentage, textinfo = "value"
                    ,marker = list(color = c("deepskyblue", "yellow", "red", "chartreuse"),
                                   line = list(width = c(1,1,1,1), color = c("deepskyblue", "yellow", "red", "lightgreen"))),
                    connector = list(line = list(color = "royalblue", dash = "dot", width = 3)), name = unique(df_use$task_id))
        funnel <- funnel %>% add_annotations(
          text = ~unique(df_use$task_id),
          x = 0.5,
          y = 3.5,
          yref = "y",
          xref = "x",
          xanchor = "middle",
          yanchor = "top",
          showarrow = FALSE,
          font = list(size = 9)
        ) 
        if (nr2 == 5) {
          md = 6
        }else {
          md = 7
        }
        if (cont1%%md!= 0) {
          funnel <- funnel %>% layout(yaxis = ax)
        }
        cont1 <<- cont1 + 1
        
        funnel
        
      })
      
      subplot(p.list, nrows = nr2) %>% layout(showlegend = FALSE)
    }
  })
  
  
  output$levelsOfDifficulty <- renderPlotly ({
    if (nchar(input$groupLevelsOfDifficulty) < 1) {}
    else {
      datosDiff <- datosDiff %>% filter(group==input$groupLevelsOfDifficulty)
      datos_melted <- datosDiff %>% melt(id.vars = c("task_id"), measure.vars = c("completed_time", "actions_completed", "p_incorrect", "p_abandoned", "norm_all_measures"), value.name = "value")
      #datos_melted$variable <- factor(datos_melted$variable, levels = c("completed_time", "actions_completed", "p_incorrect", "p_abandoned", "norm_all_measures"))
      subsetTime<-datos_melted%>% filter(variable == "completed_time")%>% mutate(value = round(value, 2))
      subsetActions<-datos_melted%>% filter(variable == "actions_completed")
      subsetIncorrect<-datos_melted%>% filter(variable == "p_incorrect")
      subsetAbandoned<-datos_melted%>% filter(variable == "p_abandoned")
      subsetGeneral<-datos_melted%>% filter(variable == "norm_all_measures")%>% mutate(value = round(value, 2))
  
      subsetTime$title = "Active Time"
      subsetActions$title2 = "Number of Actions"
      subsetIncorrect$title3 = "Percentage Incorrect"
      subsetAbandoned$title4= "Percentage Abandoned"
      subsetGeneral$title5="General Difficulty Measure"
      
      
      plotTime <-ggplot(subsetTime, aes(x=task_id, y = value)) +  geom_bar(stat='identity', position='stack') +  theme_minimal() +
        theme(axis.text.x = element_blank(),plot.title = element_text(hjust = 0.5)) + facet_wrap(~title)+
        theme(legend.position = 'bottom') + labs(title ="", x = "", y = "Time (s)")  
      

      plotAction <-ggplot(subsetActions, aes(x=task_id, y = value)) +  geom_bar(stat='identity', position='stack') +  theme_minimal() +
        theme(axis.text.x = element_blank(),plot.title = element_text(hjust = 0.5)) + facet_wrap(~title2)+
        theme(legend.position = 'bottom') + labs(title ="", x = "Action", y = "Action Measure")  
      
      plotIncorrect <-ggplot(subsetIncorrect, aes(x=task_id, y = value)) +  geom_bar(stat='identity', position='stack') +  theme_minimal() +
        theme(axis.text.x = element_blank(),plot.title = element_text(hjust = 0.5)) +facet_wrap(~title3)+
        theme(legend.position = 'bottom') + labs(title ="", x = "", y = "Incorrect Percentage")  
      
      plotAbandoned <-ggplot(subsetAbandoned, aes(x=task_id, y = value)) +  geom_bar(stat='identity', position='stack') +  theme_minimal() +
        theme(axis.text.x = element_blank(),plot.title = element_text(hjust = 0.5)) +facet_wrap(~title4)+
        theme(legend.position = 'bottom') + labs(title ="", x = "", y = "Abandoned Percentage") 
      
      plotGeneral <-ggplot(subsetGeneral, aes(x=task_id, y = value)) +  geom_bar(stat='identity', position='stack') +  theme_minimal() +
        theme(axis.text.x = element_text(angle = 90, size = 7),plot.title = element_text(hjust = 0.5)) +facet_wrap(~title5)+
        theme(legend.position = 'bottom') + labs(title ="", x = "", y = "Difficulty")  
      
      
      p1<-subplot(plotTime, plotAction,titleY = TRUE)
      p2<-subplot(plotIncorrect,plotAbandoned,titleY = TRUE)
      p3<-subplot(p1,p2,plotGeneral, nrows = 3,titleY = TRUE)
      
      
      #p_all <- subplot(plotTime, plotAction,plotIncorrect,plotAbandoned,plotGeneral, nrows=3, shareX = TRUE, shareY = TRUE, titleX = TRUE, titleY = TRUE)#%>%layout(title="Prueba")
      #p_all %>% layout(annotations = list(list(x = 1 , y = 1.05, text = "AA", showarrow = F, xref='paper', yref='paper')))
      ggplotly(p3) 
      
    }
  })
  

  output$sequenceBetweenPuzzles <- renderPlotly ({
    if (is.null(input$user)) {}
    else {
      if(nchar(input$user)>1)
      {
        
        currentSeq <<- dfSequence %>% filter(user==input$user) %>% select(-session_id) %>% mutate(user = paste("Student",  as.numeric(user)))
        
        currentSeq$funnel <<- factor(currentSeq$funnel, levels = c("completed", "submitted", "shape_created", "started"), 
                                     labels = c("Completed", "Submitted", "Shape created", "Started"))
        
        dfDifficulty1 <- datosDiff %>% filter(group == input$groupDiff) 
        datosDiff <- dfDifficulty1 %>% select(-order, -completed_time, -actions_completed, -p_incorrect, -p_abandoned, -group, -X)
        
        currentSeq <<- merge(currentSeq, datosDiff, by.x = "task_id", by.y = "task_id")
        
        dotSize = 4
        long = length(currentSeq$sequence)
        if (long < 70 && long >=55) {
          dotSize = 3
        }else if (long < 40 && long >=30) {
          dotSize = 5
        } else if (long < 30  && long >=20) {
          dotSize = 6
        } else if (long < 20  && long >=10) {
          dotSize = 7
        } else if (long < 10) {
          dotSize = 8
        }
        
        coloresVis <- c("Completed" = "green", "Submitted" = "red", "Shape created" = "yellow", "Started" = "steelblue4")
        diff <- ggplot(currentSeq, aes(x = sequence, y = norm_all_measures,  label = task_id, label2 = funnel), fill = task_id) + geom_point(aes(colour = factor(funnel)), size = dotSize) + scale_color_manual(values=coloresVis) +
          scale_y_continuous(limit = c(-0.5,1.5)) + scale_x_continuous(minor_breaks = seq(1, length(currentSeq$sequence) + 5, 1)) + labs(title ="Sequence within Puzzles", x = "Sequence", y = "Difficulty") +
          theme_minimal() + theme(axis.text.x = element_blank(), plot.title = element_text(hjust = 0.5)) + labs(color='Funnel') 
        
        ggplotly(diff, tooltip = c("x", "label","label2"), source = "S")
      }   
    }
  })
  

  
  
  output$difficultyELO <- renderPlotly({
    if (nchar(input$groupDifficulty) < 1) {}
    else {
      datosDifficultyELO <- datosDifficultyELO %>% filter(group == input$groupDifficulty)%>% mutate(difficulty = round(difficulty,2)) 
      actiDifficulty <-ggplot(datosDifficultyELO, aes(x=task_id, y = difficulty)) +  geom_bar(stat='identity', position='stack') +  theme_minimal() +  theme(axis.text.x = element_text(angle = 90, size = 7),plot.title = element_text(hjust = 0.5)) +
        theme(legend.position = 'bottom') + labs(title ="Difficulty ELO", x = "", y = "Difficulty")
      ggplotly(actiDifficulty, tooltip = c("x", "y"))
    }
  })  
  
  output$levelsOfActivity <- renderPlotly({
    if (nchar(input$userLevel) < 1) {}
    else {
      dfActivity <- dfActivity %>% mutate(value = round(value, 2)) %>% filter(user == input$userLevel) %>% select(-X, -group, -user) %>% arrange(task_id, metric) %>% filter(!(metric %in% c("move_shape", "undo_action", "redo_action", "paint", "scale_shape", "delete_shape", "rotate_view", "create_shape", "snapshot")))
      subsetEvent<-dfActivity%>% filter(metric == "event")
      subsetNevent<-dfActivity%>% filter(metric == "different_events")
      subsetActive<-dfActivity%>% filter(metric == "active_time")
      
      subsetEvent$title = "Number of Events"
      subsetNevent$title2 = "Number of Different Events"
      subsetActive$title3 = "Active Time (s)"
      
      plotEvent <-ggplot(subsetEvent, aes(x=task_id, y = value)) +  geom_bar(stat='identity', position='stack') +  theme_minimal() +  theme(axis.text.x = element_text(angle = 90, size = 7),plot.title = element_text(hjust = 0.5)) +
        theme(legend.position = 'bottom') + labs(title ="", x = "", y = "") + facet_wrap( ~ title) 
      plotDifEvent <-ggplot(subsetNevent, aes(x=task_id, y = value)) +  geom_bar(stat='identity', position='stack') +  theme_minimal() +  theme(axis.text.x = element_text(angle = 90, size = 7),plot.title = element_text(hjust = 0.5)) +
        theme(legend.position = 'bottom') + labs(title ="", x = "", y = "")+ facet_wrap( ~ title2)
      plotActive <-ggplot(subsetActive, aes(x=task_id, y = value)) +  geom_bar(stat='identity', position='stack') +  theme_minimal() +  theme(axis.text.x = element_text(angle = 90, size = 7),plot.title = element_text(hjust = 0.5)) +
        theme(legend.position = 'bottom') + labs(title ="", x = "", y = "")+ facet_wrap( ~ title3)
      
      p3<-subplot(plotActive,plotDifEvent,plotEvent, nrows = 1,shareX = TRUE,titleY = TRUE)
      p3$x$source<-"L"
      ggplotly(p3, tooltip = c("x", "y"))
    }
  })
    
    
  
  output$sequenceWP <- renderPlot ({
    if (nchar(input$sequenceWPPuzzle) < 1) {}
    else {
      currentPuzzle <<- seqWithinDf %>% filter(group_id == input$sequenceWPGroup) %>% filter(user == input$sequenceWPUser) %>% filter(task_id == input$sequenceWPPuzzle)
      
      #Vemos cuantas filas tiene para poder escalar en consecuencia
      n = 0
      filas = 0
      for (row in 1:nrow(currentPuzzle)) {
        n = n + 1
        if (n == 10 || currentPuzzle$type[row] == "submit") {
          filas = filas + 1
          n = 0
        }
      }
      
      if (length(unique(currentPuzzle$type)) == 1 && unique(currentPuzzle$type) == 'start_level') {
        plot(1:3, type='n', axes = FALSE, xlab = "", ylab = "", main = currentPuzzle$task_id[1], font.main=4, cex.main=1)
        rasterImage(pizarra, 0.5, 0, 3.3, 3.5)
        rasterImage(image_flip(no_data), 1.5, 2.9, 2.5, 2.70)
      } else {
        
        if (exists("rasterImage")) { # can plot only in R 2.11.0 and higher
          plot(1:3, type='n', axes = FALSE, xlab = "", ylab = "", main = currentPuzzle$task_id[1], font.main=4, cex.main=1)
          if (filas > 9) {
            offsetX = 0.1
            offsetY = 0.075
            xI = 1
            yI = 2.9
            limitColumn = 20
          } else if (filas >= 3) { 
            offsetX = 0.2
            offsetY = 0.15
            xI = 1
            yI = 2.9
            limitColumn = 10
          } else {
            offsetX = 0.4
            offsetY = 0.3
            xI = 1
            yI = 2.9
            limitColumn = 5
          }
          contador = 0
          rasterImage(pizarra, 0.5, 0, 3.3, 3.5)
          
          for (row in 1:nrow(currentPuzzle)) {
            if (contador == limitColumn) {
              yI = yI - offsetY
              xI = 1
              contador = 0
            }
            
            if (currentPuzzle$type[row] == "start_level") {} 
            else {
              if (currentPuzzle$type[row] == "rotate_view") {
                img_use <- rotate_view
              } else if (currentPuzzle$type[row] == "submit") {
                if (currentPuzzle$correct[row] == "True") {
                  
                  img_use <- submit_correct
                } else {
                  img_use <- submit_incorrect
                }
                
              } else if (currentPuzzle$type[row] == "snapshot") {
                
                img_use <- snapshot
                
              } else {
                stringAction <- currentPuzzle$type[row]
                figure <- currentPuzzle$shape_type[row]
                nameString <- paste(stringAction, figure, sep = "_")
                img_use <- eval(as.symbol(nameString))
                img_use <- image_annotate(img_use, currentPuzzle$shape_id[row], size = 175, gravity = "south", color = "white")
              }
              
              if (currentPuzzle$n_times[row] > 1){
                if (currentPuzzle$type[row] == "rotate_view" || currentPuzzle$type[row] == "submit" || currentPuzzle$type[row] == "snapshot"){ 
                  imgAnnotated <- image_annotate(img_use, paste( "x", currentPuzzle$n_times[row], sep= ""), size = 85, gravity = "northeast", color = "white")
                } else {
                  imgAnnotated <- image_annotate(img_use, paste( "x", currentPuzzle$n_times[row], sep= ""), size = 200, gravity = "northeast", color = "white")
                }
              } else {
                imgAnnotated <- img_use
              }
              
              #Para publicarlo hacerle el flip
              imgAnnotated <- image_flip(imgAnnotated)
              rasterImage(imgAnnotated, xI, yI, (xI+offsetX), yI - offsetY)
              
              
              
              xI = xI + offsetX
              contador = contador + 1
              
              if (currentPuzzle$type[row] == "submit") {
                if  (currentPuzzle$correct[row] == "False") {
                  xI = 1
                  yI = yI - (offsetY + 0.05)
                  contador = 0
                }
              }
            }
          }
        }
      }
    }
    
  })
  
  output$common_errPlot <- renderPlot({
    if (nchar(input$common_errPuzzle) < 1) {}
    else {
      currentGroupPuzzle <- commonErrorsDf %>% filter(group_id == input$common_errGroup) %>% filter(task_id == input$common_errPuzzle) 
      
      if (exists("rasterImage")) { # can plot only in R 2.11.0 and higher
        plot(1:3, type='n', axes = FALSE, xlab = "", ylab = "", main = currentGroupPuzzle$task_id, sub = currentGroupPuzzle$group_id, font.main=4, cex.main=1)
        
        contador = 0
        rasterImage(pizarra, 0.5, 0, 3.3, 3.5)
        rasterImage(image_flip(master_sol_img), 1.5, 2.9, 2.5, 2.70)
        currentGroupPuzzle$master_solution <- gsub("'", "\"", currentGroupPuzzle$master_solution)
        # parse the json
        mas_sol <- fromJSON(currentGroupPuzzle$master_solution)
        offsetX = 0.2
        offsetY = 0.15
        xI = 1
        yI = 2.65
        for(i in names(mas_sol)) {
          if (contador == 10) {
            yI = yI - offsetY
            xI = 1
          }
          shape <- mas_sol[[i]]
          imgsh <- eval(as.symbol(shape))
          imgsh <- image_flip(imgsh)
          rasterImage(imgsh, xI, yI, (xI+offsetX), yI - offsetY, interpolate=FALSE)
          xI = xI + offsetX
          contador = contador + 1
        }
        rasterImage(image_flip(common_errors), 1.5, yI - (offsetY*1.5), 2.5, (yI - (offsetY*3.1)))
        
        currentGroupPuzzle$common_Errors <- gsub("'", "\"", currentGroupPuzzle$common_Errors)
        # parse the json
        commonE <- fromJSON(currentGroupPuzzle$common_Errors)
        offsetX = 0.4
        offsetY = 0.3
        xI = 1
        yI = yI - (offsetY*1.75)
        contador = 0
        for(i in names(commonE)) {
          mov <- i
          if (mov == "moved_shapes") {
            mov <- "move"
          } else if (mov == "created_shapes") {
            mov <- "create"
          }  else if (mov == "deleted_shapes") {
            mov <- "delete"
          }  else if (mov == "scaled_shapes") {
            mov <- "scale"
          }  else if (mov == "rotated_shapes") {
            mov <- "rotate"
          }
          
          for (j in names(commonE[[i]])) {
            if (contador == 5) {
              yI = yI - offsetY
              xI = 1
            }
            sh <- j
            if (sh == "ramp") {
              sh = "prism"
            }
            comp_name <- paste(mov, sh, sep = "_")
            img_used <- eval(as.symbol(comp_name))
            img_used <- image_annotate(img_used, paste(commonE[[i]][[j]], "%", sep = ""), size = 150, gravity = "south", color = "white")
            img_used <- image_flip(img_used)
            rasterImage(img_used, xI, yI, (xI+offsetX), yI - offsetY, interpolate=FALSE)
            xI = xI + offsetX
            contador = contador + 1
          }
        }
      }
      
    }
  })
  
  
  
}

shinyApp(ui, server)


