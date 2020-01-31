const mongoose = require("mongoose"); //connects node.js env with mongodb server

mongoose.connect("mongodb://localhost:27017/TheParentDataBase", /*required to remove warnings xD*/{ useNewUrlParser: true }, /*if there is some error then*/(error) => {
    if (!error) {
        console.log("Now Connected to the Data Base");
    }
    else {
        console.log("Connection to Data Base Failed");
    }

}); //name of db we need to connect

const Parents = require("./course.model");