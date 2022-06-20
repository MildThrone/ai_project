import React, { useState } from 'react'
import { BiEdit } from 'react-icons/bi'
import styles from "../styles/EditQuestion.module.css"

function EditQuestion({ data, editQuestion, id, onClose }) {

    const [question, setQuestion] = useState(data.question)
    const [answer, setAnswer] = useState(data.answer)
    const [mark, setMark] = useState(data.mark)
    // console.log(data);

    return (
        <div>
            <h2>Edit Question</h2>
            <form className={styles.form}>
                <div className={styles.group}>
                    <label htmlFor="question">Question: </label>
                    <textarea
                        type="text"
                        id='question'
                        className={styles.textarea}
                        value={question}
                        onChange={
                            (event) => {
                                setQuestion(event.target.value)
                            }
                        }
                        required
                    />
                </div>
                <div className={styles.group}>
                    <label htmlFor="answer">Answer: </label>
                    <input
                        type="text"
                        id='answer'
                        className={styles.input}
                        value={answer}
                        onChange={
                            (event) => {
                                setAnswer(event.target.value)
                            }
                        }
                        required
                    />
                </div>
                <div className={styles.group}>
                    <label htmlFor="mark">Mark: </label>
                    <input
                        type="number"
                        min="0"
                        id='mark'
                        className={styles.input}
                        value={mark}
                        onChange={
                            (event) => {
                                setMark(event.target.value)
                            }
                        }
                        required
                    />
                </div>
                <div className={styles.button}>
                    <button onClick={
                        (event) => {
                            event.preventDefault()
                            editQuestion(id, question, answer, mark)
                            onClose()
                        }
                    }>
                        <BiEdit />Edit
                    </button>
                </div>
            </form>
        </div>
    )
}

export default EditQuestion