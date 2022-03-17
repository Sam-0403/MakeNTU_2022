const mongoose = require("mongoose");

const historySchema = new mongoose.Schema({
  type: {
    type: String,
    required: true,
  },
  email: {
    type: String,
    required: true,
  }
},{
  timestamps: true
});

const History = mongoose.model("History", historySchema);
module.exports = History;