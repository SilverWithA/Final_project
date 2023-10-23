import axios from "axios";

export async function signUpApi(data) {
    const response = await axios.post("http://3.36.123.174:8080/api/auth/signUp", data).catch((error) => null)
    if (!response) return null;

    const result = response.data;
    return result;
}

export const ClassicTier = async (data) => {
    const response = await axios.post("http://3.36.123.174:8080/api/classic/tier", data).catch((error) => console.log(error))
    if (!response) return null;

    const result = response.data;
    return result;
}

export const ClassicAnalysis = async (data) => {
    const response = await axios.post("http://3.36.123.174:8080/api/classic/anal", data).catch((error) => console.log(error))
    if (!response) return null;

    const result = response.data;
    console.log('result:',result);
    return result;
}

export const AramTier = async() => {
    const response = await axios.post("http://3.36.123.174:8080/api/aram/tier").catch((error) => console.log(error))
    if (!response) return null;

    const result = response.data;
    return result;
}

export const AramAnalysis = async(data) => {
    const response = await axios.post("http://3.36.123.174:8080/api/aram/anal", data).catch((error) => console.log(error))
    if (!response) return null;

    const result = response.data;
    return result;
}

export const signInApi = async (data) => {

    const response = await axios.post("http://3.36.123.174:8080/api/auth/signIn", data).catch((error) => console.log(error))
    console.log(response)
    if (!response) return null;

    const result = response.data;
    return result
}

export const widgetOneApi = async (data) => {
    const response = await axios.post("http://3.36.123.174:8080/api/widget/one", data).catch((error) => console.log(error))
    if (!response)  return null;

    const result = response.data;
    return result;

}

export const widgetTwoApi = async (data) => {
    const response = await axios.post("http://3.36.123.174:8080/api/widget/two", data).catch((error) => console.log(error))
    if (!response)  return null;

    const result = response.data;
    return result;

}
