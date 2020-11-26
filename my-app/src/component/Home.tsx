import * as React from "react"
import { Box, Input, Button, Tag } from "@chakra-ui/react";

const Home = () => {
    
    const [tweet, setTweet] = React.useState("");
    const [result, setResult] = React.useState("");
    const [tags, setTags] = React.useState<string[]>([]);

    React.useEffect(() => {
        fetch('http://localhost:5000/')
        .then(response =>  response.json())
        .then((result) => {
            setTags(Object.keys(result))
        })
        .catch(e => {
            console.log("ERROR ", e);
        })
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
            setResult(result['tweet'])
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
    <Box>
        <p>Palabras que pueden ayudarte a encontrar lo que buscas:</p>
    {
        tags.map(tag => <Tag>{tag}</Tag> )
    }
    </Box>
    
    <br/>
    {
        result && 
        <Box>
            {result}
        </Box>
    }
  </Box>
}

export default Home;