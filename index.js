import {useState} from "react";
import ProductCard from "../components/ProductCard";
export default function Home(){
 const [q,setQ]=useState("");
 const [res,setRes]=useState([]);
 const search=async()=>{
  const r=await fetch(`http://localhost:5000/api/search?q=${q}`);
  setRes(await r.json());
 };
 return (<div style={{padding:40}}>
 <h1>Smart Product Discovery</h1>
 <input value={q} onChange={e=>setQ(e.target.value)} />
 <button onClick={search}>Search</button>
 {res.map(p=><ProductCard key={p.id} product={p}/>)}
 </div>);
}