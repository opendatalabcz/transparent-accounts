interface Config {
  API_URL: string
}

const Config: Config = {
  API_URL: String(process.env.REACT_APP_API_URL)
}

export default Config;
