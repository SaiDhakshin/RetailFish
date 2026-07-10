import axios from "axios";

export default axios.create({
    baseURL: "http://localhost/api",
    timeout: 30000,
});