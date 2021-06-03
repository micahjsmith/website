Title: Evaluating the impact of mentorship programs
Date: 2021-06-02
Category: life
Slug: evaluating-the-impact-of-mentorship-programs
Authors: Micah Smith
Status: draft

One initiative that I have been working on for the past year at MIT is the [EECS Graduate Application Assistance Program](https://www.thrive-eecs.mit.edu/gaap) (EECS GAAP), a program that pairs underrepresented applicants to the MIT EECS department with graduate student mentors.

This program is motivated by the understanding that some applicants to graduate school are privileged to have networks of experienced mentors who can give them advice about applying to different programs and feedback on their application materials. This mentorship might be part of the "hidden curriculum" that allows applicants to put the right spin on their application. Meanwhile, underrepresented students usually have fewer mentorship opportunities even if they have just as strong of a CV. Can we level the playing field by connecting these students with mentors? In EECS GAAP, applicants and their mentors worked closely together during the Fall 2020 application period on their application strategy, statement of purpose, CV, and other materials to best portray their existing experience and skills to the admissions committee.

Together with several other student leaders and many volunteers, we have recently wrapped up our first year.  I encourage you to learn more about our program by reading our [launch post](https://www.thrive-eecs.mit.edu/news-eecs-gaap-launch) or [press coverage from MIT News](https://news.mit.edu/2020/gaap-mentorship-encourages-underrepresented-students-eecs-1013).  Our program is one of many that have been sprouting up around the US in computer science departments and other departments, and there is a long history of mentorship programs in computer science, academia more broadly, and other areas.

**Today, I want to write about one technical problem that arises in mentorship programs. That is, do they work?**

In the context of application assistance programs, applicants and their mentors invest a lot of time and effort in working together. For applicants, they have to bring mentors into their confidence to share their background and the materials that go into their application, some of which may be quite personal. For mentors, they have to carve time out of their busy research schedules to read and edit statements of purpose and try to provide good advice. There are many benefits of mentorship programs to applicants and mentors beyond admissions outcomes. But at the end of the day, we hope that these investments are worth it in terms of addressing some of the inequities that lead some students to be underrepresented in certain academic spaces.

### Challenges in evaluating mentorship programs

We would like to answer the question, does participation in a mentorship program help students be admitted to graduate programs?

However, there are many challenges to evaluating the impact and efficacy of mentorship programs.

1. *Confounding factors.* There are many factors that make it more difficult for underrepresented students to be admitted, not just the lack of mentorship. Thus a student from an underrepresented background may be less likely to be admitted than a student from a privileged background, even if they both have access to mentorship.

1. *Selection bias.* We might look at the admissions rate of students who participate in the mentorship program compared to similar students who do not participate. However, the decision to seek out and participate in a mentorship program may indicate that the student is already more "attuned" to graduate school applications and may be already more likely to be admitted regardless of their participation.

1. *Privacy and confidentiality.* If a student participates in a mentorship program that is targeted at certain groups, such as LGBTQ+ individuals, then revealing their participation would be outing them in a sensitive context. For this and other reasons, programs like EECS GAAP make strict pledges to preserve the privacy and confidentiality of students. For example, we commit to never sharing any information about participants in our program with the EECS Department or the EECS Graduate Office without their explicit consent. (Which in turn, we only asked for one time, which was to share with administrative staff to process application fee reimbursements.) And to certainly never share this information with any faculty or staff involved in the admissions process.

Ultimately, this means that even computing the admissions rate of participants in our program is a challenge, let alone doing any causal inference.

### One solution

I recently came up with one method that would help conduct a robust analysis of the causal impact of participating in a mentorship program on admissions, addressing to the challenges above. This method has some drawbacks but would be a valuable tool for program designers.

It relies on two things: a capacity limitation in mentorship programs, and algorithms for private set intersection cardinality computation.

Let $m$ be the number of students who can be offered mentors in a program (i.e. due to a limited number of mentors who are volunteering). Let $n$ be the number of students who apply to participate in the program.

#### Control groups

If a student is deemed to be eligible to the program, then accept them at random with probability $m/n$. This leads to a treatment group (offered a mentor) of size $m$ and a control group (not offered a mentor) of size $n-m$. Given this randomization, we can assume that latent characteristics of the two groups are similar.

#### Secure computation of admissions numbers

We want to compute the following quantities:

| Value | Description |
| --- | --- |
| $s^t$ | the number of students in the treatment group who actually submit their application to the department |
| $s^c$ | the number of students in the control group who actually submit their application to the department |
| $a^t$ | the number of students in the treatment group who are admitted to the department |
| $a^c$ | the number of students in the control group who are admitted to the department |
| $e^t$ | the number of students in the treatment group who enroll in the department |
| $e^c$ | the number of students in the control group who enroll in the department |

To do so without violating the privacy and confidentiality of the students (in either group!), we can use algorithms for [private set intersection](https://en.wikipedia.org/wiki/Private_set_intersection) (PSI), with optimizations for private set intersection cardinality (PSIC), given that we do not need to know the intersecting elements (and indeed, revealing intersecting elements to the admissions officers would violate confidentiality).

This is not my area of expertise, but I did a brief literature review, and found that there are many algorithms for PSI. Applications include private contact list discovery and private advertising conversion detection.

For example, [Freedman, Nissim, and Pinkas](https://www.cs.princeton.edu/~mfreed/docs/FNP04-pm.pdf) present a variety of protocols for *private matching* including derivative problems like private set intersection cardinality (which they call private cardinality matching). These protocols are based on existing homomorphic encryption systems, which are cryptosystems that preserve the group homomorphism of addition and allows multiplication by a constant. Preserving the group homomorphism of addition means that given Enc($m_1$) and Enc($m_2$), the encryptions of two secret values, one can efficiently compute Enc($m_1 + m_2$) without knowledge of the private key. Preserving multiplication by a constant is designed similarly. The elements in the set are encoded in domain of a fixed size and then represented as the roots of a polynomial. The coefficients of the polynomial are encrypted and sent to a counterparty, who does some additional operations involving evaluating the polynomial on their own inputs, multiplying and adding by carefully chosen values, and encrypting the result. The cardinality protocol is described in Section 4.4 of the paper.

Much recent work (using improved techniques compared to homomorphic encryption) seems to focus on providing efficient algorithms, secure against malicious actors, or supporting multiple parties. We have a very simple use case with a small dataset (on the order of thousands), no malicious actors, and only two parties.

There are several open-source implementations of PSIC protocols. For example, [Garimella et al](https://eprint.iacr.org/2021/243.pdf) provide a [C++ implementation](https://github.com/osu-crypto/PSI-analytics) of PSIC (as well as other functions of the intersection) based on *oblivious transfer* that can compute the cardinality of intersection on $2^{12}$ = 4,096 items in around 8 seconds with about 3MB of communication. (There were 3,742 applicants to MIT EECS in 2020). [OpenMined/PSI](https://github.com/OpenMined/PSI) also implements PSIC based on elliptic-curve Diffie-Helman and Golomb-coded sets (but does not include a reference to a proof of security). I'm sure there are other implementations that I didn't find in my limited search.

If there was a trusted third party that could compare the sets of names directly, we wouldn't have to resort to these efforts, but given the sensitivity of the admissions data, it is unlikely such a party could be agreed upon.

#### Statistical tests

Let's focus on the outcome of admissions, but we can repeat the same analysis for other outcomes. Let $A^t$ be a random variable equal to $1$ if a treated student is admitted and $0$ otherwise, and let $A^c$ be a corresponding random variable for control students.

Then $\bar{A^t} = \frac{a^t}{m}$ is the sample mean of $A^t$ and $\bar{A^c} = \frac{a^c}{n-m}$ is the sample mean of $A^c$. The null hypothesis is that the means of $A^t$ and $A^c$ are identical, i.e. that there is no difference in the admission rate between GAAP participants vs a control group with similar characteristics.

We can reasonably assume that the variance of $A^t$ and $A^c$ are similar. Thus we can use a simple [independent two-sample t-test](https://en.wikipedia.org/wiki/Student%27s_t-test#Equal_or_unequal_sample_sizes,_similar_variances_(1/2_%3C_sX1/sX2_%3C_2)).

The test statistic $t$ is given by

$$
t = \frac{
    \frac{a^t}{m} - \frac{a^c}{n-m}
}{
    s_p \cdot \sqrt{\frac{1}{m} + \frac{1}{n-m}}
}
$$

where

$$
s_p = \sqrt{\frac{(m-1) s^2_t + (n-m-1) s^2_c}{n - 2}}
$$

is an estimator of the pooled standard deviation of the two samples.

Now we can obtain standard p-values from $t$.

Using SciPy:

```python
from scipy.stats import ttest_ind_from_stats
mean1 = at/m
mean2 = ac/(n-m)
std1 = mean1 * (1-mean1) ** 2 + (1-mean1) * mean1 ** 2
std2 = mean2 * (1-mean2) ** 2 + (1-mean2) * mean2 ** 2
t, p = ttest_ind_from_stats(mean1, std1, m, mean2, std2, n-m)
```

### Some hypotheses

I'll now pre-register hypotheses without having done this type of analysis.

* **H1**: $A^t > A^c$. This is the most important hypothesis. If not, the fundamental thesis of application assistance programs is basically wrong and it's difficult to justify the effort put into the program.
* **H2**: $S^t > S^c$. If this hypothesis is not confirmed, it's not a big deal. One could obtain this result without using expert mentors (i.e. the nagging parents effect). It could also be that students realize through working with their mentors that the program is not the right fit for them for whatever reason and they should focus their efforts elsewhere.
* **H3**: $E^t > E^c$. If not, then the effects of mentors in "selling" the program are not strong, but this is where other DEI efforts should come into play (generally creating a more inclusive campus, having programming at visit days targeted to underrepresented students, etc.).

### Drawbacks and limitations

There are several drawbacks to this method that program designers should consider carefully.

1. *Capacity limitation.* This method exploits the fact that a program may only be able to serve a limited number of applicants in order to create a control group. However, if there is no capacity limitation, then ethically a program should probably serve all eligible students rather than artificially introducing a limit in order to form a control group.

1. *Random prioritization.* To form a valid control group, applicants should be randomly assigned to be accepted and matched with a mentor versus to be rejected. However, this conflicts with other approaches to prioritization in the face of capacity limits, such as prioritizing based on underrepresented background (i.e., some backgrounds may be "more underrepresented" than others).

1. *Timing effects.* It would be great if all eligible students applied to the program at the beginning of the application cycle. In reality, students begin their graduate school applications at different points, and may find out about the mentorship program at different points during the cycle. If students arrive to the program consistently throughout the cycle, then randomly accepting a student conflicts with first-come-first-served approaches. While in one sense it is equally arbitrary to accept a student at random or due to when they happen to submit some application form, the end result is still that each applicant/mentor pair has less time to work together, on average.

1. *Group programming.* In EECS GAAP at MIT, once we had matched all available mentors with applicants, we scrambled to support the students who continued applying to our program with other types of resources. This included group mentoring sessions, short office hour-style appointments, and custom application support materials. Thus instead of rejecting applicants to form a control group, a program may want to accept them but offer group programming like this. Now our method would be comparing the efficacy of one-on-one mentoring versus group programming, which is not quite what we are interested in. Some group programming like application support materials may also be made available to the applicants with mentors which would partially alleviate this concern, yet they may take advantage of it differentially (i.e. pay less attention to a FAQ section in a document if they can just bounce questions off of their mentor directly).

### Qualitative outcomes

We may also like to answer other questions about the effects on applicants and mentors in more qualitative outcomes like sentiment towards graduate school, confidence in application materials, and connectedness to the community. There are challenges in evaluating these outcomes as well, which are usually assessed from surveys. These include "differential attrition", low response rates, and response linking.

### Conclusion

The organizers of application assistance programs should evaluate the impacts of their program and be open to the negative finding that such programs do not positively influence admissions outcomes. The method described here is one way of rigorously evaluating this.

Have you seen research evaluating the impact of mentorship programs in admissions? Do you have any feedback on the method in this post? Let me know in the comments.
