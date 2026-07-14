import axios from "axios";

export default axios.create({
  baseURL: "http://localhost/api",
  timeout: 3000000, //5mins
});
