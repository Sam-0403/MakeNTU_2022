require("dotenv").config();
const express = require("express");
const mongoose = require("mongoose");
const passport = require("passport");
const flash = require("express-flash");
const session = require("express-session");
const methodOverride = require("method-override");
const MongoStore = require('connect-mongo');
const User = require("./models/User");
const History = require("./models/History");
const bcrypt = require("bcryptjs");
const bodyParser = require("body-parser")
const {
  checkAuthenticated,
  checkNotAuthenticated,
} = require("./middlewares/auth");

const app = express();

const initializePassport = require("./passport-config");
initializePassport(
  passport,
  async (email) => {
    const userFound = await User.findOne({ email });
    return userFound;
  },
  async (id) => {
    const userFound = await User.findOne({ _id: id });
    return userFound;
  }
);

app.set("view engine", "ejs");
app.use(express.urlencoded({ extended: true }));
app.use(bodyParser.urlencoded({ extended: false }));
app.use(flash());
app.use(
  session({
    store: new MongoStore({mongoUrl: `${process.env.DB_URL}`}),
    secret: process.env.SESSION_SECRET,
    resave: false,
    saveUninitialized: false,
  })
);
app.use(passport.initialize());
app.use(passport.session());
app.use(methodOverride("_method"));
app.use(express.static("public"));

app.get("/", checkAuthenticated, (req, res) => {
  res.render("index", {
    name: req.user.name,
    email: req.user.email
  });
});

app.get("/register", checkNotAuthenticated, (req, res) => {
  res.render("register");
});

app.get("/login", checkNotAuthenticated, (req, res) => {
  res.render("login");
});

app.get("/history/:email", async (req, res) => {
  const history = await History.findOne({email: req.params.email}).sort({ _id: -1 });
  if(history){
    res.send(history);
  }
  else{
    res.send({type: '尚無資料'});
  }
});

app.get("/python", checkAuthenticated, (req, res) => {
  console.log("Login");
  res.send({
    name: req.user.name,
    email: req.user.email
  });
});

app.get("/pythonFail", checkAuthenticated, (req, res) => {
  console.log("Login Fail");
  res.send({
    name: 'None',
    email: 'None'
  });
});

app.post(
  "/login",
  checkNotAuthenticated,
  passport.authenticate("local", {
    successRedirect: "/",
    failureRedirect: "/login",
    failureFlash: true,
  })
);

app.post("/register", checkNotAuthenticated, async (req, res) => {
  const userFound = await User.findOne({ email: req.body.email });

  if (userFound) {
    req.flash("error", "User with that email already exists");
    res.redirect("/register");
  } else {
    try {
      const hashedPassword = await bcrypt.hash(req.body.password, 10);
      const user = new User({
        name: req.body.name,
        email: req.body.email,
        password: hashedPassword
      });

      await user.save();
      res.redirect("/login");
    } catch (error) {
      console.log(error);
      res.redirect("/register");
    }
  }
});

app.post("/sendData", async (req, res) => {
  var type = req.body.type;
  var email = req.body.email;

  const userFound = await User.findOne({ email: req.body.email });
  if(userFound){
    const history = new History({
      type: type,
      email: email
    });
    await history.save();
    res.send("Send Data Success!");
  }
})

app.post(
  "/userLogin",
  checkNotAuthenticated,
  passport.authenticate("local", {
    successRedirect: "/python",
    failureRedirect: "/pythonFail",
    failureFlash: true,
  })
);

app.delete("/logout", (req, res) => {
  req.logOut();
  res.redirect("/login");
});

mongoose
  .connect(`${process.env.DB_URL}`, {
    useUnifiedTopology: true,
    useNewUrlParser: true,
  })
  .then(() => {
    app.listen(process.env.PORT || 8000, () => {
      console.log("Server is running on Port 8000");
    });
  });
