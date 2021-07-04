import * as React from "react"
import { Box, Input, Button, Tag } from "@chakra-ui/react";

const Home = () => {
    
    const [tweet, setTweet] = React.useState("");
    const [result, setResult] = React.useState([]);

    React.useEffect(() => {
        // fetch('http://localhost:5000/')
        // .then(response =>  response.json())
        // .then((result) => {
        //     setTags(Object.keys(result))
        // })
        // .catch(e => {
        //     console.log("ERROR ", e);
        // })
    }, [])

    const searchTweet = () => {
        fetch('http://localhost:5000/', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({'search':tweet})
        })
        .then(response =>  response.json())
        .then((result) => {
            console.log(result)
            console.log(result.sort(function (a: any, b: any): any {
             return a[1] < b[1] 
            }));
            setResult(result)
        })
        .catch(e => {
            console.log("ERROR ", e);
        })
    }

    return <Box>
    <Box display="flex">
        <Input placeholder="Escribe el tweet" onChange={e=>setTweet(e.target.value)}/>
        <Button colorScheme="blue" onClick={searchTweet}>Buscar Tweet</Button>
    </Box>
    <br/>
    <br/>
    {
        result && result.map((tweet, idx) => 
        <Box key={idx}>
            <b>{idx+1}</b>. {tweet[0]}
        </Box>)
        
    }
  </Box>
}

export default Home;