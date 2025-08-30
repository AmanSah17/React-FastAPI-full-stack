import React, {useState,useEffect} from 'react'
import api from './api'

const App = () => {
  const [transactions, setTransactions] = useState([])
  const [formData , SetFormData] = useState(
    {
      amount: '' , 
      category : '' , 
      description : '',
      is_income : false,
      date: '',

    

    }
  );
}


export default App;
