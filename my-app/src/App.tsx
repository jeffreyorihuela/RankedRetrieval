import * as React from "react"
import {
  ChakraProvider,
  theme,
  Box,
  Heading,
} from "@chakra-ui/react"
import { ColorModeSwitcher } from "./ColorModeSwitcher"
import { Logo } from "./Logo"
import Home from "./component/Home"

export const App = () => (
  <ChakraProvider theme={theme}>
    <Box padding="35px 20px">
      <Box display="flex" justifyContent="center" height="100px">
        <Logo />
      </Box>
      <br/>
      <Heading>Bienvenido a Tweet Ranked de las elecciones 2018</Heading>
      <br/>
      <Home/>
    </Box>
    
  </ChakraProvider>
)
