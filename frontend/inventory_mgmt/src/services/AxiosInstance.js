import axios from "axios";
import authHeader from "./AuthHeader";

let instance = axios.create({
  baseURL: "http://localhost:8000",
  headers: authHeader(),
});

export default instance;
