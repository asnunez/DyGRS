
import axios from 'axios';

export class APIHandler{
    constructor(url) {
        this.url = url;
    }
    getUrl() {
        return this.url;
    }
    listStreams() {
        return axios.get(`${this.url}/list`).then((res) => {
            return res.data.map(
                ({ uri }) => `${this.url}${uri}`,
            );
        });
    }
    listAlerts() {
        return axios.get(`${this.url}/alerts`).then((res) => {
            return res.data.map(
                ({ id,camera,type,timestamp }) => `Id: ${id}, Cámara: ${camera}, Tipo: ${type}, Timestamp: ${timestamp}`,
            );
        });
    }
    getCams(){
        return axios.get(`${this.url}/horus`);
    }
    startStream(uri) {
        return axios.post(`${this.url}/start`, {uri});
    }
}
