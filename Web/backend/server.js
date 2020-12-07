const express = require("express");
const app = express();
const server = require("http").createServer(app);
const PORT = 8003;
const io = require("socket.io")(server);
const cors = require("cors");
const {sequelize, Sensing1} = require("./models");
const { randomArray } = require("./utils/random");

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({extended: false}));

sequelize.sync({force: false})
.then(() => console.log("Successfully connected to Database!"))
.catch((err) => console.log(err));

app.get("/", (req, res) => {
    return res.json({connection: "this server in running"})
});

io.on("connection", function(socket){
    let offset = 0;
    setInterval(async () => {
        // socket.emit("chat", {
        //     first: randomArray(),
        //     second: randomArray()
        // });
        try{
            const dataLength = await Sensing1.findAndCountAll({
                attributes: [sequelize.fn("COUNT", sequelize.col("id"))]
            });
            // console.log(dataLength);
            const data = await Sensing1.findAll({
                limit: 24,
                offset: offset
            });
            // console.log(data);
            offset+=24;

            const array = data.reduce((acc, cur) => {
                acc.push({time: cur.dataValues.time, num1: cur.dataValues.num1, num2: cur.dataValues.num2});
                return acc;
            }, []);
            socket.emit("chat", array);
            if(offset > dataLength.count - 24){
                offset = 0;
            }
            console.log(array);
        }catch(error){
            console.log(error);
        }
    }, 1000);
    socket.on("chat", function(data){
        // console.log(`message from client : ${data}`);
    })
})

server.listen(PORT, () => console.log(`this server listening on ${PORT}`));