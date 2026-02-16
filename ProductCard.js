export default function ProductCard({product}){
 return(<div style={{border:'1px solid #ddd',padding:10,margin:10}}>
 <h3>{product.title}</h3><p>{product.category}</p></div>);
}