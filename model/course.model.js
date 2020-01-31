const mongoose = require("mongoose");

var MySchema = new mongoose.Schema({
    ParentName: {
        type: String,
        required: "Required"
    },
    Password: {
        type: String,
        required: "Required"
    },
    ChildPresence: {
        type: String,
        required: "Required"
    },
    UserName: {
    type: String,
    required: "Required"
    }

});//Create a schema because mongo is schema less!!!

mongoose.model("Parents", MySchema) // This collection named Parents will require schema MySchema to be stored