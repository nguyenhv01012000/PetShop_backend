import Axios from 'axios'
import React, { useContext, useEffect, useState } from 'react'
import { withRouter } from 'react-router-dom';
import '../../App.css'
import { UserContext } from '../../contexts/User';
import '../../Styles/Login.css'

function Login(props) {

    const { 
        setUserInfoFunc 
    } = useContext(UserContext);

    const [tab, setTab] = useState(0)
    const [email, setEmail] = useState("")
    const [name, setName] = useState("")
    const [password, setPassword] = useState("")
    const [arrSuccess, setArrSuccess] = useState()
    const [arrErr, setArrErr] = useState() 

    useEffect(()=> {
        Axios.get(`http://pe.heromc.net:4000/users/${localStorage.getItem('user-id')}`, { 
            headers: {"authorization" : `Bearer ${localStorage.getItem('token')}`}
        })
        .then(res => { 
            setUserInfoFunc(res.data.user);
            props.history.push("/account")
        })
        .catch(err => {
            console.log(err);
        })
    },[]) 

    const sendAccount = (event) => {
        event.preventDefault()
        if (tab === 0) {
            Axios.post('http://localhost:8000/api/login/', {
                username: email,
                password: password
            }) 
            .then(res => {
                setArrSuccess("Đăng nhập thành công!") 
                setArrErr("");
                // setTimeout(()=> {
                //     window.location.reload(false);
                //     document.body.style.overflow = 'unset';
                // }, 1000)
                props.history.push('')
                localStorage.setItem('token', res.data.token);
                localStorage.setItem('user-id', res.data.user.id);
            })
            .catch(err => {
                setArrSuccess("");
                setArrErr("Tên đăng nhập hoặc mật khẩu không chính xác");
            })
        } else {
            Axios.post('http://localhost:8000/api/register/', {
                username: name,
                email: email,
                password: password,
                //userRole: "user"
            })
            .then(res => { 
                setArrSuccess("Đăng ký thành công!")
                setArrErr("");
                setTimeout(()=> {
                    window.location.reload(false);
                    document.body.style.overflow = 'unset';
                }, 1000)
            })
            .catch(err => { 
                setArrSuccess("");
                setArrErr(err.response.data.username);
            })
        }
    }

    return (
        <div className="login flex-col">
            <div className="login-title">
                <strong>Thiết bị định vị</strong> cho chó và mèo
            </div>
            <div className="login-banner"> 
            </div>
            { tab === 0 &&
                <div className="login-box flex-col">
                    <div className="login-box-title"><strong>Đăng</strong> nhập</div>
                    <div className="login-status">
                        { arrErr && <div className="login-err">{arrErr}</div>}
                        { arrSuccess && <div className="login-success">{arrSuccess}</div>}
                    </div>
                    <form className="flex-col" onSubmit={sendAccount}>
                        <label>Tên Đăng Nhập</label>
                        <input
                            value={email}
                            onChange={(event)=>{
                                setEmail(event.target.value)
                            }}
                        ></input>
                        <label>Mật khẩu</label>
                        <input
                            value={password}
                            onChange={(event)=>{
                                setPassword(event.target.value)
                            }}
                        ></input>
                        <button>Đăng nhập</button>
                    </form>
                    <div className="login-forgot">Quên mật khẩu?</div>
                    <div className="login-register" onClick={()=>{setTab(1)}}>Tạo tài khoản mới</div>
                </div>
            }
            { tab === 1 &&
                <div className="login-box flex-col">
                    <div className="login-box-title"><strong>Tạo</strong> tài khoản</div>
                    <div className="login-status">
                        { arrErr && <div className="login-err">{arrErr}</div>}
                        { arrSuccess && <div className="login-success">{arrSuccess}</div>}
                    </div>
                    <form className="flex-col" onSubmit={sendAccount}>
                        <label>Tên *</label>
                        <input
                            value={name}
                            onChange={(event)=>{
                                setName(event.target.value)
                            }}
                        ></input>
                        <label>Email *</label>
                        <input
                            value={email}
                            onChange={(event)=>{
                                setEmail(event.target.value)
                            }}
                        ></input>
                        <label>Mật khẩu *</label>
                        <input
                            value={password}
                            onChange={(event)=>{
                                setPassword(event.target.value)
                            }}
                        ></input>
                        <button>Tạo tài khoản</button>
                    </form> 
                    <div className="login-register" onClick={()=>{setTab(0)}}>Đã có tài khoản?</div>
                </div>
            }
        </div>
    )
}
export default withRouter(Login)