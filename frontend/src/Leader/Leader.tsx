import Response from "../Response/Response";
import TEST_DATA from "./TEST_DATA";
import { GetFormInfo} from "../Response/API2Front";
import {useEffect, useState} from "react";
import {ResponseDataInterface} from "../Response/ResponseData";
import {Navigate, useParams} from "react-router-dom";

function Leader(): JSX.Element {
    const [loaded, setLoaded] = useState(false);
    const [data, setData] = useState(TEST_DATA);
    const params = useParams();
    console.log("rendering")
    useEffect( () => {
        let id = params.id
        if (id !== undefined) {
            GetFormInfo(+id as number).then((responseData) => {
                setLoaded(true);
                console.log(responseData)
                setData(responseData);
            })
        }

    }, [])
    if (!loaded) {
        return <div>Loading...</div>
    }
    return <Response {...data as ResponseDataInterface}/>
}

export default Leader;